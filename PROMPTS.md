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

### P6 (2026-10-27): GitHub repo review

**Prompt:**
> i have created my github repo https://github.com/L00205332/workrepo and it has 3 files i believe
> you can access it

**LLM response (summary):** Read-only inspection of the repo with the GitHub CLI: visibility,
files, commit authorship, merged PRs, collaborators. Confirmed all commits are authored by me and
that the lecturer appears as a collaborator, then proposed how to clone it locally and lay out the
assignment (keeping the brief PDF out of the public repo).

**My action:** _(fill in)_

---

### P7 (2026-10-27): Repo cloned and renamed, project setup files

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

### P8 (2026-10-27): Keep the repo name

**Prompt:**
> i won't rename the repo as it's shared with Ruth my instructor.

**LLM response (summary):** Agreed. The repo stays `L00205332/workrepo`, and the existing remote
URL is already correct, so no changes are needed.

**My action:** Kept the original repo name so the link shared with my instructor stays stable.

---

### P9 (2026-10-27): Static website template (Part A(a) baseline)

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

### P10 (2026-10-27): Where is the three-tier architecture?

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

### P11 (2026-10-27): Three-tier template (Part A(b) baseline)

**Prompt:** _(answers to the design questions in P10)_
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

### P12 (2026-10-27): Difference between Part A(a) and Part A(b)

**Prompt:**
> what's the difference between Part A(a) and Part A(b)?

**LLM response (summary):** Compared the two parts: A(a) is a static website (fixed files
in S3, served by CloudFront, with no server code and no database); A(b) is a dynamic
application split into web, application and database tiers inside a VPC. Covered what each
demonstrates, its cost and how it scales, and when each style is the right choice.

**My action:** _(fill in)_

---

### P13 (2026-10-27): Push and merge before deploying

**Prompt:**
> let me push and merge the code changes for the two designs before we actually try to deploy on
> AWS

**LLM response (summary):** Checked the working tree and gave the branch, commit, push and PR
commands to merge the static-site and three-tier templates as two separate PRs.

**My action:** _(fill in)_

---

### P14 (2026-10-31): Code review first; always destroy resources

**Prompt:**
> let me review the code first before we start deploying the stacks. also add to the project's md
> that we always need to destroy the resources once we have finished, it's a free account after
> all.

**LLM response (summary):** Added an "always destroy the stacks" notice at the top of the README
and a new section 10.1 with commands that confirm nothing is left running (stacks, EC2, RDS,
load balancers, snapshots). Also filled in my name in the README header and corrected the
repository structure, which listed folders that don't exist. Gave a review guide for the two
templates.

**My action:** Decided to review both templates myself before any deployment and made clean-up
after every session a project rule.

---

### P15 (2026-10-31): Restructure into two projects with modules

**Prompt:**
> the code looks solid but i don't like the distribution of the files, let's consider the static
> site and the the three tier as two separate projects inside the same repo, for each project we
> need to have main.tf where we actually run the code, and for the resources let's have modules
> like , compute(e.g. ec2 instances, ec2 auto scaling), networking (e.g. vpc, subnets, subnet
> groups, security groups), database (e.g. RDS) and definitely you will need variables/parameters
> file, what do you think ?

**LLM response (summary):** Agreed with the modular layout. Pointed out that `main.tf` is
Terraform naming; the CloudFormation equivalent is a root template (`main.yaml`) that composes
**nested stacks** (`AWS::CloudFormation::Stack`) as modules, packaged with
`aws cloudformation package`, plus JSON parameter files per environment. Proposed a folder
layout for both projects, listed the trade-offs (an S3 bucket is needed for packaged templates;
there is an extra packaging step), and asked for confirmation before refactoring.

**My action:** Chose the modular layout (two projects, each a root stack plus modules and a
parameters file), added a separate `loadbalancer` module for the web tier, and decided that I run
every command myself.

---

### P16 (2026-10-31): Implement the modular refactor

**Prompt:**
> yes go ahead, add the loadbalancer module and apply other suggestions but always remember i will
> be the one to run the commands, you just provide the code

**LLM response (summary):** Refactored both single-file templates into nested-stack projects:
- `static-site/`: `main.yaml` plus modules `storage`, `cdn` (CloudFront, OAC and bucket policy)
  and `content` (Lambda deployer), and `parameters/dev.json`
- `three-tier/`: `main.yaml` plus modules `networking` (VPC, subnets, route tables, security
  groups, endpoints), `loadbalancer` (ALB, target group, listener), `compute` (IAM, launch
  template, ASG, scaling) and `database` (subnet group, RDS), and `parameters/dev.json`
- Input validation stays in the root stacks; modules pass outputs to each other with
  `!GetAtt <Module>Stack.Outputs.<Name>`
- Removed the old `templates/` folder. Updated `.cfnlintrc.yaml` to lint every root and module
  template, and to ignore W3002 (local `TemplateURL`, intended for `package`). Added explicit
  `DeletionPolicy` to the nested stacks (I3011).
- Updated the README: repo structure, a "how nested stacks are deployed" section,
  `package` + `deploy` commands with parameter files, and the artifacts-bucket setup and
  clean-up.

Checks: cfn-lint clean. A script confirmed every parameter passed to a module is declared,
every required module parameter is passed, every `Outputs` reference exists, the parameter
files only use known keys, and the embedded app code is unchanged. The suggestion to move the
app code out of user data was deferred, as agreed. No commands were run against AWS or git.

**My action:** _(fill in)_

---

### P17 (2026-10-31): Deploy the static site

**Prompt:**
> PR merged, let's start deploying the static site to AWS.

**LLM response (summary):** Gave the step-by-step PowerShell commands for me to run: sync
`main` and create a testing branch, lint, create the artifacts bucket, package, deploy, read the
outputs, and run four `curl` checks (HTTPS 200 with security headers, HTTP→HTTPS redirect,
custom 404, direct S3 access denied). Also gave troubleshooting commands for nested-stack
failures and a reminder to destroy the stack afterwards.

**My action:** _(fill in)_

---

### P18 (2026-10-31): Deploy from main

**Prompt:**
> i won't deploy from a branch let's deploy from main

**LLM response (summary):** Agreed: deploys run from `main`, the reviewed and merged code, and
a branch is only created when a file needs to change (fixes or test evidence). Gave the
commands to switch to `main` and deploy.

**My action:** Decided to always deploy from `main` and use branches only for code or
documentation changes.

---

### P19 (2026-10-31): "Next level" improvements and CI pipeline

**Prompt:**
> for next level, i would:
> GitHub Actions: cfn-lint (+ cfn-nag) on every PR
> Either using Aurora or atleast make the RDS multi-az
> Create notifications based on resources metrics
> Move the Python app out of user data into three-tier/app/

**Follow-up decisions (my answers to the LLM's questions):** Multi-AZ RDS only (not Aurora);
alert email passed as a command-line override so it never lands in the public repo; CI fails
on errors only (warnings reported, not blocking).

**LLM response (summary):** Planned the four improvements as separate branches and PRs, CI
first so the others are checked automatically. Implemented the first one:
`.github/workflows/cfn-validate.yml`, with two jobs:
- `cfn-lint` (pinned 1.58.0, fails only on errors)
- `cfn-nag` (scans each project's `*.yaml` templates, fails only on FAILURES)

The workflow token is read-only, and stale runs are cancelled. Added a documented cfn-nag
suppression for RDS deletion protection (F80) in the database module, a CI badge, and a CI
section in README 6.5. cfn-nag could not be run locally (no Ruby), so its first run is on the PR.

**My action:** _(fill in)_

---

### P20 (2026-10-31): PR strategy and cfn-nag policy

**Prompts:**
> why 4 PRs ? why can't we create 1 branch for all changes ?

> two PRs (CI, then the rest)

> i don't like cfn-nag it's causing a lot of problems

> Option B

**LLM response (summary):** Explained the trade-off between one PR per feature (matches the
brief's "regular PRs", easier review and rollback, isolated testing) and a single branch (less
overhead, one paid AWS test session). Suggested a middle ground: CI first, then one branch with
one commit per feature. After cfn-nag's first FAILURE (F24, fixed by making the DB username
`NoEcho`), listed four options: keep cfn-nag with branch protection, make it report-only,
replace it with Checkov, or remove it. Implemented option B: the cfn-nag job is advisory
(`continue-on-error: true`), and cfn-lint errors still block merges.

**My action:** Chose two PRs (CI, then the remaining features as separate commits on one
branch) and made cfn-nag advisory, keeping the F24 fix.

---

### P21 (2026-10-31): Move the application out of user data

**Prompt:** _(feature 4 of the list in P19, implemented on `feature/next-level`)_
> Move the Python app out of user data into three-tier/app/

**LLM response (summary):**
- Extracted the app into `three-tier/app/app.py` and `three-tier/app/app.service`, formatted
  with ruff.
- The compute module's user data is now a short bootstrap. It downloads the release from
  `s3://<artifacts>/three-tier/app/<AppVersion>/` through the S3 gateway endpoint.
- Added the `ArtifactsBucketName` and `AppVersion` (semver) parameters, plus an IAM policy that
  is scoped to that single release prefix.
- Because `AppVersion` is part of the user data, bumping it triggers a rolling instance update.
- Added an `app lint (ruff)` CI job, pinned to ruff 0.6.9 and targeting Python 3.9 (Amazon
  Linux 2023).
- Updated the README: structure, an "Application releases" section, and the upload step in the
  deployment instructions.

**My action:** _(fill in)_

---

### P22 (2026-10-31): Multi-AZ RDS

**Prompt:**
> committed, go ahead with Multi-AZ RDS

**LLM response (summary):**
- `DBMultiAZ` now defaults to `true` in the root stack and in `parameters/dev.json`.
- Added explanatory comments on Multi-AZ failover behaviour to the database module, plus
  non-overlapping off-peak windows: backups `02:00-03:00` and maintenance
  `sun:03:30-sun:04:30` (UTC).
- Exposed the RDS instance identifier as a new `DatabaseInstanceId` output, so failover can be
  tested and the database monitored.
- README: the architecture diagram now shows the primary and standby, with a note that every
  tier spans both AZs. Added a "Database high availability" section (synchronous standby,
  automatic failover, how the app behaves during failover, maintenance, and the cost trade-off
  against Aurora). Updated the deploy-time (about 20 minutes) and cost (about $3-4/day)
  estimates.
- cfn-lint passes.

**My action:** _(fill in)_

---

### P23 (2026-10-31): Monitoring, alerting, access logs and flow logs

**Prompt:**
> committed, include the access logs and flow logs too

**LLM response (summary):**
- **New `monitoring` module:** an SNS topic with an email subscription (`AlertEmail` is a
  `NoEcho` root parameter with email validation, passed on the command line and never stored
  in the repo), and 9 CloudWatch alarms:
  - ALB: ELB 5xx, target 5xx, unhealthy hosts, slow responses
  - Auto Scaling group: CPU high
  - RDS: CPU, free storage, freeable memory, connections

  Every alarm also sends an OK notification. An RDS event subscription emails failover,
  failure, availability and low-storage events. Wired in as the fifth nested stack, created
  last.
- **Networking module:** VPC Flow Logs (ALL traffic) to a CloudWatch Logs group with 14-day
  retention. The IAM role is scoped to that log group and has an `aws:SourceAccount` condition.
- **Loadbalancer module:** ALB access logs to a private, encrypted S3 bucket. Only the
  regional ELB account may write to the `alb/` prefix, and objects expire after 30 days. A
  Lambda custom resource empties the bucket on stack deletion, and `DependsOn` ordering
  removes the ALB before the bucket is emptied. New outputs give the ALB and target group
  names in CloudWatch dimension format.
- **cfn-nag:** W52 and W60 are now resolved. W56 (HTTP listener) and W47 (unencrypted SNS
  topic) are suppressed with written reasons.
- **README:** structure, module table, creation order, a "Monitoring, alerting and logging"
  section, deploy commands that add `AlertEmail` to the `dev.json` values (bash and
  PowerShell, checked locally), the cfn-nag table and the clean-up notes.
- cfn-lint passes. All module parameters and outputs were cross-checked.

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
