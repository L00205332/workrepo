# ATU CloudFormation Assignment: L00205332

**Module:** IaC for DevOps Pipelines, Atlantic Technological University
**Student:** Mohamed Hanafi Sayed Khalifa Ismail (L00205332)
**Lecturer:** Ruth Lennon

This README is the lab write-up for the assignment.

> [!IMPORTANT]
> **Always destroy the stacks when you finish.** This project runs on a free-tier AWS account
> with limited credits. Every deploy session ends with the clean-up steps in
> [section 10](#10-clean-up), followed by a check that nothing is left running. The three-tier
> stack costs about $2-3 per day while it exists, even when idle.

---

## 1. Overview

_TODO: a short summary of what the project delivers._

- **Part A(a):** a static website hosted from S3 and served publicly, with my L-number and name as the header.
- **Part A(b):** a three-tier architecture (web, application, database tiers).
- **Part B:** best practices, tooling and the "ilities" (security, scalability, performance).

## 2. Repository structure

```
.
├── static-site/                # Part A(a): S3 + CloudFront static website
│   ├── main.yaml               # root stack, wires the modules together
│   ├── modules/
│   │   ├── storage.yaml        # private, encrypted S3 bucket
│   │   ├── cdn.yaml            # CloudFront + OAC + bucket policy
│   │   └── content.yaml        # Lambda custom resource that publishes the pages
│   └── parameters/dev.json     # parameter values for the dev environment
├── three-tier/                 # Part A(b): web, application and database tiers
│   ├── main.yaml               # root stack, wires the modules together
│   ├── modules/
│   │   ├── networking.yaml     # VPC, subnets, route tables, security groups, VPC endpoints
│   │   ├── loadbalancer.yaml   # web tier: Application Load Balancer
│   │   ├── compute.yaml        # application tier: EC2 Auto Scaling group + app
│   │   └── database.yaml       # database tier: RDS PostgreSQL
│   └── parameters/dev.json
├── .cfnlintrc.yaml             # cfn-lint configuration (lints every template)
├── PROMPTS.md            # Declared tutorials and LLM prompts
└── README.md             # This write-up
```

## 3. Prerequisites

- An AWS account with a non-root IAM identity (root user MFA enabled, budget alarm configured)
- AWS CLI v2 with a named profile
- [cfn-lint](https://github.com/aws-cloudformation/cfn-lint)

### 3.1 How the projects are deployed (nested stacks)

Each project is a **root stack** (`main.yaml`) that composes **modules**. Each module is a
nested stack (`AWS::CloudFormation::Stack`), the CloudFormation equivalent of a Terraform
module. One module's outputs are passed as another module's parameters, and those links set
the creation and deletion order.

Nested stack templates must be in S3, so deployment has two steps:

1. `aws cloudformation package` uploads each module to an artifacts bucket and writes a
   `packaged-main.yaml` whose `TemplateURL`s point at S3. The file is git-ignored.
2. `aws cloudformation deploy` creates or updates the root stack from the packaged file, with
   the values in `parameters/<env>.json`.

Create the artifacts bucket once. It must have a globally unique name:

```bash
aws s3 mb s3://l00205332-cfn-artifacts-eu-west-1 --profile atu --region eu-west-1
```

> Commands are shown in bash style. In PowerShell, replace the trailing `\` line
> continuations with a backtick (`` ` ``), or put each command on one line.

## 4. Part A(a): Static website on S3

### 4.1 Architecture

```
Visitor --HTTPS--> CloudFront distribution  (cdn module)
                     | HTTP -> HTTPS redirect, HTTP/2+3, gzip/brotli,
                     | managed security headers, custom 404 page
                     |
                     | requests signed with Origin Access Control (SigV4)
                     v
                   Private S3 bucket  (storage module)
                     encrypted (SSE-S3), versioned, all public access blocked,
                     bucket policy: read only by this distribution, TLS only
                     ^
                     | writes index.html, error.html, styles.css on create/update
                     | empties the bucket on delete
                   Lambda custom resource  (content module)
```

The root stack [`static-site/main.yaml`](static-site/main.yaml) creates three nested stacks:

| Module | Purpose | Key resources |
|--------|---------|---------------|
| [`storage.yaml`](static-site/modules/storage.yaml) | Stores the web pages | `AWS::S3::Bucket` |
| [`cdn.yaml`](static-site/modules/cdn.yaml) | Public-facing web service over HTTPS | `AWS::CloudFront::Distribution`, `AWS::CloudFront::OriginAccessControl`, `AWS::S3::BucketPolicy` |
| [`content.yaml`](static-site/modules/content.yaml) | Publishes the page content at deploy time | `AWS::Lambda::Function`, `AWS::IAM::Role`, `AWS::Logs::LogGroup`, `Custom::WebsiteContent` |

The header shows `L00205332 – Mohamed Hanafi Sayed Khalifa Ismail`. Both values come from
[`static-site/parameters/dev.json`](static-site/parameters/dev.json), so the page content is
never hard-coded in the templates.

### 4.2 Deployment

Root stack: [`static-site/main.yaml`](static-site/main.yaml), modules in
[`static-site/modules/`](static-site/modules/)

```bash
# Lint first (uses .cfnlintrc.yaml)
cfn-lint

# 1. Upload the modules to S3 and write the packaged root template
aws cloudformation package \
  --profile atu --region eu-west-1 \
  --template-file static-site/main.yaml \
  --s3-bucket l00205332-cfn-artifacts-eu-west-1 \
  --s3-prefix static-site \
  --output-template-file static-site/packaged-main.yaml

# 2. Create or update the stack. CAPABILITY_IAM is needed because the content
#    module creates the IAM role for the deployer Lambda.
aws cloudformation deploy \
  --profile atu --region eu-west-1 \
  --stack-name l00205332-static-site-dev \
  --template-file static-site/packaged-main.yaml \
  --parameter-overrides file://static-site/parameters/dev.json \
  --capabilities CAPABILITY_IAM \
  --tags Project=atu-cloudformation Owner=L00205332 Environment=dev

# Print the website URL
aws cloudformation describe-stacks \
  --profile atu --region eu-west-1 \
  --stack-name l00205332-static-site-dev \
  --query "Stacks[0].Outputs[?OutputKey=='WebsiteURL'].OutputValue" --output text
```

The first deployment takes about 5 minutes, mostly while the CloudFront distribution is created.

### 4.3 Testing

Deployed on 2026-10-31 to `eu-west-1` from the `main` branch, as stack `l00205332-static-site-dev`.

#### Package and deploy

`cfn-lint` passed with no findings. The artifacts bucket was created once. `package` uploaded
the three modules to S3 and wrote `packaged-main.yaml`. `deploy` created the stack from that file
with the values in `parameters/dev.json`. Running `aws s3 mb` a second time returned
`BucketAlreadyOwnedByYou`, which confirms the bucket already existed and only needs creating once.

![Terminal: cfn-lint, artifacts bucket, package and deploy](docs/images/static-site/01-package-and-deploy.png)

#### Nested stacks in the CloudFormation console

With **View nested** turned on, the console shows the root stack and its three module stacks,
all in `CREATE_COMPLETE`. The creation times show the order that the module dependencies
enforce: **storage** (12:06:41), then **cdn** (12:07:04), which needs the bucket, then
**content** (12:10:34), which needs both the bucket and the CloudFront distribution. Most of the
deploy time is spent creating the CloudFront distribution.

![CloudFormation console: root stack and three nested module stacks](docs/images/static-site/02-cloudformation-nested-stacks.png)

#### Stack outputs

The root stack exposes the website URL, the generated bucket name and the CloudFront
distribution ID. The bucket name is generated by CloudFormation, which avoids global naming
collisions.

![Stack outputs: BucketName, WebsiteURL, DistributionId](docs/images/static-site/03-stack-outputs.png)

| Output | Value |
|--------|-------|
| WebsiteURL | `https://dd045i4kaiewg.cloudfront.net` |
| BucketName | `l00205332-static-site-dev-storagesta-websitebucket-xuuvrhfuxhx4` |
| DistributionId | `E1QAVV4JD92NWB` |

> These resources are destroyed after testing (see [section 10](#10-clean-up)), so the URL no
> longer works.

#### The live website

The site opened in a browser at the CloudFront URL (`https://dd045i4kaiewg.cloudfront.net`).
This shows that the whole path works:
- CloudFront served `index.html` as the default root object, over HTTPS.
- It fetched the page from the **private** S3 bucket using Origin Access Control.
- The page content was the one written by the Lambda content deployer.

The header shows **L00205332 – Mohamed Hanafi Sayed Khalifa Ismail**, as the assignment
requires. The deployment details (stack `l00205332-static-site-dev`, region `eu-west-1`,
environment `dev`) were filled in by CloudFormation at deploy time from the stack parameters
and pseudo-parameters, so they are not hard-coded in the HTML.

![Live static website served by CloudFront with the L-number and name in the header](docs/images/static-site/04-website.png)

#### Functional and security checks

All four checks passed:

![curl output: HTTP request redirected to HTTPS by CloudFront](docs/images/static-site/05-curl-http-redirect.png)

![curl output: HTTPS 200 with security headers, custom 404, direct S3 access 403](docs/images/static-site/06-curl-https-checks.png)

> **Note on Windows `curl.exe`:** the HTTPS checks first printed nothing, because `-s` hides
> errors. Windows curl (Schannel) could not complete the certificate revocation check from this
> network. Adding `-S` (show errors) and `--ssl-no-revoke` fixed it. This was a client-side
> issue; the site itself served HTTPS correctly, as the browser test confirms.

| # | Check | Command | Expected | Result |
|---|-------|---------|----------|--------|
| a | Site served over HTTPS with security headers | `curl.exe -sSI --ssl-no-revoke https://dd045i4kaiewg.cloudfront.net/` | `200`, with `strict-transport-security`, `x-frame-options`, `x-content-type-options` | ✅ `200 OK`, `Content-Type: text/html; charset=utf-8`, `Strict-Transport-Security: max-age=31536000`, `X-Frame-Options: SAMEORIGIN`, `X-Content-Type-Options: nosniff`, `x-amz-server-side-encryption: AES256` (object encrypted at rest), `Server: AmazonS3` behind `Via: ... (CloudFront)` |
| b | HTTP redirected to HTTPS | `curl.exe -sI http://dd045i4kaiewg.cloudfront.net/` | `301` to `https://` | ✅ `301 Moved Permanently`, `Location: https://dd045i4kaiewg.cloudfront.net/`, `X-Cache: Redirect from cloudfront`. The managed security headers (`X-Frame-Options`, `X-Content-Type-Options`, `X-XSS-Protection`, `Referrer-Policy`) are already present on the redirect. |
| c | Custom error page for missing pages | `curl.exe -sSI --ssl-no-revoke https://dd045i4kaiewg.cloudfront.net/nope.html` | `404` | ✅ `404 Not Found` with `Content-Length: 446` (the custom `error.html`, not S3's XML error) and `X-Cache: Error from cloudfront`. S3's `403` for the missing key was mapped to a `404` by the distribution's `CustomErrorResponses`. |
| d | Bucket not publicly readable | `curl.exe -sSI --ssl-no-revoke https://l00205332-static-site-dev-storagesta-websitebucket-xuuvrhfuxhx4.s3.eu-west-1.amazonaws.com/index.html` | `403` | ✅ `403 Forbidden` from S3. The object exists, but it can only be read through CloudFront (OAC), never directly. |

## 5. Part A(b): Three-tier architecture

### 5.1 Architecture

Root stack: [`three-tier/main.yaml`](three-tier/main.yaml), modules in
[`three-tier/modules/`](three-tier/modules/)

```
                    Internet
                       |  HTTP :80
          +------------v-------------+   VPC 10.0.0.0/16, 2 Availability Zones
WEB TIER  |  Application Load Balancer|   public subnets  10.0.0.0/24, 10.0.1.0/24
          +------------+-------------+
                       |  :8080 (ALB security group only)
          +------------v-------------+
APP TIER  |  EC2 Auto Scaling group   |   private subnets 10.0.2.0/24, 10.0.3.0/24
          |  Python UI + JSON API     |   no internet route; S3 + Secrets Manager endpoints
          +------------+-------------+
                       |  :5432 TLS (app security group only)
          +------------v-------------+
DB TIER   |  RDS PostgreSQL           |   isolated subnets 10.0.4.0/24, 10.0.5.0/24
          +--------------------------+
```

| Path | Tier | What it does |
|------|------|--------------|
| `/` | App, via the web tier | HTML page showing which instance and AZ served the request |
| `/api/health` | App | Health check used by the ALB (does not touch the DB) |
| `/api/visits` | App + DB | Inserts a row in PostgreSQL and returns the visit count |

| Module | Tier | Contents |
|--------|------|----------|
| `networking.yaml` | All | VPC, 6 subnets, route tables, Internet Gateway, security groups, VPC endpoints |
| `loadbalancer.yaml` | Web | Application Load Balancer, target group, HTTP listener |
| `compute.yaml` | Application | IAM role, launch template (with the app in user data), Auto Scaling group, scaling policy |
| `database.yaml` | Database | DB subnet group, RDS PostgreSQL instance |

Creation order: `networking`, then `database` and `loadbalancer` in parallel, then `compute`.

_TODO: my explanation of the design decisions._

### 5.2 Deployment

```bash
cfn-lint

aws cloudformation package \
  --profile atu --region eu-west-1 \
  --template-file three-tier/main.yaml \
  --s3-bucket l00205332-cfn-artifacts-eu-west-1 \
  --s3-prefix three-tier \
  --output-template-file three-tier/packaged-main.yaml

aws cloudformation deploy \
  --profile atu --region eu-west-1 \
  --stack-name l00205332-three-tier-dev \
  --template-file three-tier/packaged-main.yaml \
  --parameter-overrides file://three-tier/parameters/dev.json \
  --capabilities CAPABILITY_IAM \
  --tags Project=atu-cloudformation Owner=L00205332 Environment=dev

aws cloudformation describe-stacks \
  --profile atu --region eu-west-1 \
  --stack-name l00205332-three-tier-dev \
  --query "Stacks[0].Outputs[?OutputKey=='ApplicationURL'].OutputValue" --output text
```

The first deployment takes about 15 minutes (RDS is the slowest resource). Running cost is
about $2-3 per day (ALB, 2 x t4g.micro, db.t4g.micro, Secrets Manager endpoint), so delete
the stack after testing.

### 5.3 Testing
_TODO_

## 6. Part B: Best practices and "ilities"

### 6.1 Security
_TODO_

### 6.2 Scalability
_TODO_

### 6.3 Performance
_TODO_

### 6.4 Cost
_TODO_

### 6.5 Code quality and tooling
_TODO: linting, comments, parameterisation, CI._

## 7. Taking it to the next level

_TODO: how I extended or improved on the tutorial and LLM baseline (assignment Part A, Q2)._

## 8. Workflow: branches and pull requests

_TODO: describe the branching strategy and list the PRs._

## 9. Declared tutorials and LLM usage

All tutorials and LLM prompts used are declared in [PROMPTS.md](PROMPTS.md).

## 10. Clean-up

```bash
# Deleting a root stack also deletes all of its nested (module) stacks.

# Static site: the content deployer Lambda empties the bucket automatically on delete.
aws cloudformation delete-stack --profile atu --region eu-west-1 --stack-name l00205332-static-site-dev
aws cloudformation wait stack-delete-complete --profile atu --region eu-west-1 --stack-name l00205332-static-site-dev

# Three-tier: RDS keeps a final snapshot (DeletionPolicy: Snapshot). Delete it afterwards.
aws cloudformation delete-stack --profile atu --region eu-west-1 --stack-name l00205332-three-tier-dev
aws cloudformation wait stack-delete-complete --profile atu --region eu-west-1 --stack-name l00205332-three-tier-dev
aws rds describe-db-snapshots --profile atu --region eu-west-1 --snapshot-type manual \
  --query "DBSnapshots[].DBSnapshotIdentifier" --output text
aws rds delete-db-snapshot --profile atu --region eu-west-1 --db-snapshot-identifier <snapshot-id>

# At the end of the module (not every session): remove the artifacts bucket and its contents
aws s3 rb s3://l00205332-cfn-artifacts-eu-west-1 --force --profile atu --region eu-west-1
```

### 10.1 Confirm nothing is left running

Run these after every session. Each command should return an empty result.

```bash
# No project stacks left (deleted stacks are not listed)
aws cloudformation list-stacks --profile atu --region eu-west-1 \
  --stack-status-filter CREATE_COMPLETE UPDATE_COMPLETE ROLLBACK_COMPLETE DELETE_FAILED \
  --query "StackSummaries[?starts_with(StackName,'l00205332')].StackName" --output text

# No running EC2 instances, RDS databases, load balancers or leftover snapshots
aws ec2 describe-instances --profile atu --region eu-west-1 \
  --filters Name=instance-state-name,Values=pending,running,stopping,stopped \
  --query "Reservations[].Instances[].InstanceId" --output text
aws rds describe-db-instances --profile atu --region eu-west-1 --query "DBInstances[].DBInstanceIdentifier" --output text
aws elbv2 describe-load-balancers --profile atu --region eu-west-1 --query "LoadBalancers[].LoadBalancerName" --output text
aws rds describe-db-snapshots --profile atu --region eu-west-1 --snapshot-type manual --query "DBSnapshots[].DBSnapshotIdentifier" --output text
```

If a stack ends in `DELETE_FAILED`, open its **Events** tab in the CloudFormation console, fix the
blocking resource (for example, empty a bucket by hand), then delete the stack again.

## 11. References

_TODO_
