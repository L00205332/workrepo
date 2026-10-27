# Declared Tutorials and LLM Prompts

The assignment brief (Part A, Q2) requires every tutorial and LLM prompt used to be declared.
This file is the running log. It is copied or linked into `README.md` at submission.

## LLM tools used

| Tool | Model | Interface | Purpose |
|------|-------|-----------|---------|
| Claude Code | Claude Opus 5.5 (`claude-opus-5-5`) | Claude desktop app (Code tab) | Environment setup, scaffolding of basics, explanation and review |

## Tutorials and references followed

| # | Date | Title / Source | URL | What was used | How I extended it |
|---|------|----------------|-----|---------------|-------------------|
| T1 | 2026-10-22 | AWS Lambda docs: Infrastructure as code (quoted in the brief) | https://docs.aws.amazon.com/lambda/latest/dg/foundation-iac.html | Background on CloudFormation as the foundational IaC service | n/a (reading only) |

## Prompt log

Each entry records the prompt exactly as typed, a short summary of the response, and what I
then did with it myself (accepted, changed, rejected) so that my own contribution is clear.

### P1 (2026-10-27): Assignment kick-off

**Prompt:**
> I am starting my CloudFormation Assignment here and you Claude Code is going to help me.

**LLM response (summary):** Read the assignment PDF, summarised the deliverables (Part A static
site + 3-tier stack, Part B best practices, submission rules), flagged the rule that all commits
must be authored by me, and proposed a repo layout and branch plan.

**My action:** Agreed to work through setup first; chose to keep this prompt log.

---

### P2 (2026-10-27): Environment setup and prompt log

**Prompt:**
> we need first to do the needed setup to make sure that you have access to my course AWS account
> and my github as well. I haven't created the AWS account using my ATU account though and we might
> need to work on that together. as you may know I will need to have all my used prompts when
> submitting my assignment so i would suggest creating and using PROMPTS.md for declared
> tutorials + LLM prompts create that now.

**LLM response (summary):** Created this `PROMPTS.md`, checked which local tools were installed
(git, GitHub CLI, AWS CLI, cfn-lint), and listed the account and credential setup steps for me
to do myself.

**My action:** _(fill in)_

---

### P3 (2026-10-27): AWS account choice

**Prompt:**
> I will setup my AWS account to be opened with your ATU email

**LLM response (summary):** Gave a step-by-step guide for opening a personal AWS account with my
ATU email: securing the root user, setting a cost budget alarm, creating an admin user in IAM
Identity Center, and logging in from the CLI with an SSO profile instead of long-lived access keys.

**My action:** _(fill in)_

---

### P4 (2026-10-27): AWS account progress update

**Prompt:**
> cool I have created atu-L00205332 root AWS account and can see 100 USD credits, I have enabled
> root MFA, I have also created L00205332-admin with MFA enabled

**LLM response (summary):** Checked local tool and CLI profile status, confirmed which setup
steps were done and which were still open (budget alarm, CLI SSO profile), and asked whether the
admin user was made in IAM Identity Center or as a classic IAM user.

**My action:** _(fill in)_

---

### P5 (2026-10-27): Setup validation commands

**Prompt:**
> ok i have finished github,cfn and aws configure, list me the validation commands before we move

**LLM response (summary):** Listed the commands that check the setup (git identity, GitHub CLI
auth, cfn-lint, AWS profile and caller identity, CloudFormation access) and ran them to report
the results.

**My action:** _(fill in)_

---

### P6 (2026-10-27): cfn-lint not on PATH

**Prompt:**
> all valdiation commands have worked perfectly except:
> `cfn-lint --version` → "The term 'cfn-lint' is not recognized as the name of a cmdlet..."
> (PowerShell error output pasted)

**LLM response (summary):** Explained that pip installed cfn-lint into the per-user Python
Scripts folder, which is not on PATH, and gave a PowerShell command that adds that folder to the
user PATH, plus a fallback that works without changing PATH.

**My action:** _(fill in)_

---

### P7 (2026-10-27): GitHub repo review

**Prompt:**
> i have created my github repo https://github.com/L00205332/workrepo and it has 3 files i believe
> you can access it

**LLM response (summary):** Read-only inspection of the repo with the GitHub CLI: visibility,
files, commit authorship, merged PRs, collaborators. Confirmed all commits are authored by me and
that the lecturer appears as a collaborator, then proposed how to clone it locally and lay out the
assignment (keeping the brief PDF out of the public repo).

**My action:** _(fill in)_

---

### P8 (2026-10-27): Repo cloned and renamed, project setup files

**Prompt:**
> I have run `git clone https://github.com/L00205332/workrepo.git` (clone output pasted)
> and i have renamed our repo from the settings to be atu-cloudformation-L00205332

**LLM response (summary):** Moved this `PROMPTS.md` into the repo and drafted the project setup
files for my review: `.gitignore` (blocks credentials and local artefacts), `.gitattributes`
(consistent line endings), `.cfnlintrc.yaml` (lint config) and a `README.md` skeleton for the lab
write-up. Gave me the git commands to update the remote URL after the rename and to commit on a
`chore/project-setup` branch with a PR.

**My action:** _(fill in)_

---

### P9 (2026-10-27): `gh` not recognised when creating the PR

**Prompt:**
> `gh pr create --base main --title "chore: project setup" ...` → "The term 'gh' is not recognized
> as the name of a cmdlet..." (PowerShell error output pasted)

**LLM response (summary):** Checked the repo state: the commit and the push of
`chore/project-setup` had worked. Found that the repo was still named `workrepo` on GitHub (the
rename had not been saved) and the remote still pointed there. Explained that the terminal had
not picked up the new PATH and gave fixes: open a new terminal, or call `gh` by its full path, or
open the PR in the browser.

**My action:** _(fill in)_

---

### P10 (2026-10-27): Keep the repo name

**Prompt:**
> i won't rename the repo as it's shared with Ruth my instructor.

**LLM response (summary):** Agreed. The repo stays `L00205332/workrepo`, and the existing remote
URL is already correct, so no changes are needed.

**My action:** Kept the original repo name so the link shared with my instructor stays stable.

---

### P11 (2026-10-27): Static website template (Part A(a) baseline)

**Prompt:**
> PR merged, use Mohamed Hanafi Sayed Khalifa Ismail in the header alongside L00205332 for our
> website

**LLM response (summary):** Generated the baseline `templates/static-site.yaml`:
- a private S3 bucket (SSE-S3 encryption, all public access blocked, ACLs disabled, versioning,
  30-day expiry of old versions, TLS-only bucket policy)
- CloudFront with Origin Access Control, HTTPS redirect, HTTP/2+3, compression, the AWS-managed
  CachingOptimized cache policy and SecurityHeaders response policy, and a custom 404 page
- a Lambda-backed custom resource that writes `index.html`, `error.html` and `styles.css` (name
  and L-number injected from parameters), invalidates the cache on update and empties the bucket
  on delete; its log group has 14-day retention
- outputs for the URL, bucket and distribution ID

Linted clean with cfn-lint (after adding explicit `DeletionPolicy`/`UpdateReplacePolicy` for
rule I3011) and passed `aws cloudformation validate-template`. Also added deploy and clean-up
commands to the README.

**My action:** _(fill in: what I reviewed, changed or extended)_

---

### P12 (2026-10-27): Where is the three-tier architecture?

**Prompt:**
> where is the three tier architecture here? all i could see is CDN(Frontend), Lambda
> function(writes the web pages into the bucket at deploy time and empties the bucket on stack
> deletion) with S3 stores the the site content, where is the frontend? where is the API? where is
> the database ?

**LLM response (summary):** Clarified that the brief asks for two separate setups: Part A(a), the
static S3 website just built (not three-tier; its Lambda is deployment tooling, not an
application tier), and Part A(b), a second template for the web, application and database tiers
that had not been built yet. Proposed design options for Part A(b), with cost trade-offs, and
asked me to choose one.

**My action:** Chose the classic VPC design (ALB, EC2 Auto Scaling, RDS, no NAT Gateway) and
kept the three-tier stack separate from the static site, as the brief describes two setups.

---

### P13 (2026-10-27): Three-tier template (Part A(b) baseline)

**Prompt:** _(answers to the design questions in P12)_
> Classic VPC (Recommended); Keep separate (Recommended)

**LLM response (summary):** Generated the baseline `templates/three-tier.yaml`:
- **Network:** a VPC across 2 AZs with 6 subnets (public / app / db), separate route tables,
  and no NAT Gateway; private access goes through an S3 gateway endpoint, a Secrets Manager
  interface endpoint, and optional SSM endpoints
- **Security groups:** chained Internet → ALB:80 → App:8080 → DB:5432; the DB and endpoint
  groups have no egress
- **Web tier:** an internet-facing ALB that drops invalid headers
- **App tier:** an Auto Scaling group (t4g.micro, AL2023 arm64) using IMDSv2 and encrypted
  gp3 volumes, with a rolling update policy and a CPU target-tracking scaling policy. It runs
  a small Python app (UI at `/`, `/api/health`, `/api/visits`) as a non-root systemd service
  and reads DB credentials from Secrets Manager.
- **DB tier:** RDS PostgreSQL 18 (encrypted, private, password managed by RDS in Secrets
  Manager, 7-day backups, snapshot on delete)

cfn-lint flagged PostgreSQL 16 as deprecated (W3691), so the template was changed to 18, the
current default in eu-west-1. Passed cfn-lint and `validate-template`; the embedded Python was
syntax-checked. Added the architecture, deploy and clean-up sections to the README.

**My action:** _(fill in: what I reviewed, changed or extended)_

---

### P14 (2026-10-27): Difference between Part A(a) and Part A(b)

**Prompt:**
> what's the difference between Part A(a) and Part A(b)?

**LLM response (summary):** Compared the two parts: A(a) is a static website (fixed files
in S3, served by CloudFront, with no server code and no database); A(b) is a dynamic
application split into web, application and database tiers inside a VPC. Covered what each
demonstrates, its cost and how it scales, and when each style is the right choice.

**My action:** _(fill in)_

---

### P15 (2026-10-27): Push and merge before deploying

**Prompt:**
> let me push and merge the code changes for the two designs before we actually try to deploy on
> AWS

**LLM response (summary):** Checked the working tree and gave the branch, commit, push and PR
commands to merge the static-site and three-tier templates as two separate PRs.

**My action:** _(fill in)_

---

<!-- Template for new entries:

### Pn (YYYY-MM-DD): Short title

**Prompt:**
> exact prompt text

**LLM response (summary):** ...

**My action:** what I kept, changed or rejected, and why.

---
-->
