"""Application tier for the three-tier demo.

Serves a small UI at "/" (rendered by the browser) and a JSON API:
  GET /api/health  - liveness check for the load balancer (no DB call)
  GET /api/visits  - records a visit in PostgreSQL and returns the total
"""

import html
import json
import os
import subprocess
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

DB_HOST = os.environ["DB_HOST"]
DB_PORT = int(os.environ.get("DB_PORT", "5432"))
DB_NAME = os.environ["DB_NAME"]
DB_SECRET_ARN = os.environ["DB_SECRET_ARN"]
REGION = os.environ["AWS_REGION"]
STUDENT_ID = os.environ["STUDENT_ID"]
STUDENT_NAME = os.environ["STUDENT_NAME"]

_credentials = None
_schema_ready = False


def instance_metadata(path):
    """Read EC2 instance metadata using IMDSv2 (session token required)."""
    token_req = urllib.request.Request(
        "http://169.254.169.254/latest/api/token",
        method="PUT",
        headers={"X-aws-ec2-metadata-token-ttl-seconds": "60"},
    )
    token = urllib.request.urlopen(token_req, timeout=2).read().decode()
    req = urllib.request.Request(
        "http://169.254.169.254/latest/meta-data/" + path,
        headers={"X-aws-ec2-metadata-token": token},
    )
    return urllib.request.urlopen(req, timeout=2).read().decode()


INSTANCE_ID = instance_metadata("instance-id")
AVAILABILITY_ZONE = instance_metadata("placement/availability-zone")


def get_credentials(refresh=False):
    """Fetch the DB username/password from Secrets Manager (cached)."""
    global _credentials
    if _credentials is None or refresh:
        result = subprocess.run(
            [
                "aws",
                "secretsmanager",
                "get-secret-value",
                "--secret-id",
                DB_SECRET_ARN,
                "--region",
                REGION,
                "--query",
                "SecretString",
                "--output",
                "text",
            ],
            check=True,
            capture_output=True,
            text=True,
            timeout=15,
        )
        _credentials = json.loads(result.stdout)
    return _credentials


def connect():
    """Open a TLS connection to PostgreSQL.

    If login fails, the cached secret may be stale because RDS rotates
    it, so fetch it again and retry once.
    """
    import psycopg2  # lazy import: /api/health works even without the driver

    for attempt in range(2):
        creds = get_credentials(refresh=attempt > 0)
        try:
            return psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                dbname=DB_NAME,
                user=creds["username"],
                password=creds["password"],
                sslmode="require",
                connect_timeout=5,
            )
        except psycopg2.OperationalError:
            if attempt == 1:
                raise


def record_visit():
    """Insert a visit row and return the total number of visits."""
    global _schema_ready
    conn = connect()
    try:
        with conn, conn.cursor() as cur:  # commits on success
            if not _schema_ready:
                cur.execute(
                    "CREATE TABLE IF NOT EXISTS visits ("
                    " id SERIAL PRIMARY KEY,"
                    " served_by TEXT NOT NULL,"
                    " visited_at TIMESTAMPTZ NOT NULL DEFAULT now())"
                )
                _schema_ready = True
            # Parameterised query: never build SQL from strings.
            cur.execute("INSERT INTO visits (served_by) VALUES (%s)", (INSTANCE_ID,))
            cur.execute("SELECT count(*) FROM visits")
            return cur.fetchone()[0]
    finally:
        conn.close()


PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{sid} | Three-tier demo</title>
  <style>
    body {{ margin: 0; font-family: system-ui, sans-serif; background: #f7f9f9; color: #1d2b2a; }}
    header {{ background: #00594f; color: #fff; padding: 2rem 1rem; text-align: center; }}
    header h1 {{ margin: 0 0 .5rem; }}
    main {{ max-width: 760px; margin: 2rem auto; padding: 0 1rem; }}
    .tier {{ background: #fff; border-left: 4px solid #00594f; padding: .75rem 1rem; margin: .75rem 0; }}
    code {{ background: #e6eeed; padding: .1rem .35rem; border-radius: 4px; }}
  </style>
</head>
<body>
  <header>
    <h1>{sid} &ndash; {name}</h1>
    <p>Three-tier architecture on AWS, provisioned with CloudFormation</p>
  </header>
  <main>
    <div class="tier"><strong>Web tier:</strong> Application Load Balancer (public subnets)</div>
    <div class="tier"><strong>Application tier:</strong> EC2 <code>{iid}</code> in <code>{az}</code> (private subnet)</div>
    <div class="tier"><strong>Database tier:</strong> RDS PostgreSQL (isolated subnets)
      &ndash; total visits: <strong id="visits">loading&hellip;</strong></div>
    <p>Refresh the page: the load balancer spreads requests across instances in both AZs.</p>
  </main>
  <script>
    fetch("/api/visits")
      .then(function (r) {{ return r.json(); }})
      .then(function (d) {{ document.getElementById("visits").textContent = d.visits !== undefined ? d.visits : d.error; }})
      .catch(function () {{ document.getElementById("visits").textContent = "unavailable"; }});
  </script>
</body>
</html>
"""


class Handler(BaseHTTPRequestHandler):
    def _send(self, status, body, content_type="application/json"):
        data = body if isinstance(body, bytes) else json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        if self.path == "/api/health":
            self._send(200, {"status": "ok", "instance": INSTANCE_ID})
        elif self.path == "/api/visits":
            try:
                self._send(
                    200,
                    {
                        "visits": record_visit(),
                        "served_by": INSTANCE_ID,
                        "availability_zone": AVAILABILITY_ZONE,
                    },
                )
            except Exception as err:  # do not leak internals to the client
                self.log_error("database error: %s", err)
                self._send(503, {"error": "database unavailable"})
        elif self.path == "/":
            page = PAGE.format(
                sid=html.escape(STUDENT_ID),
                name=html.escape(STUDENT_NAME),
                iid=html.escape(INSTANCE_ID),
                az=html.escape(AVAILABILITY_ZONE),
            )
            self._send(200, page.encode(), "text/html; charset=utf-8")
        else:
            self._send(404, {"error": "not found"})


if __name__ == "__main__":
    ThreadingHTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
