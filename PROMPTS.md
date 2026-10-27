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

<!-- Template for new entries:

### Pn (YYYY-MM-DD): Short title

**Prompt:**
> exact prompt text

**LLM response (summary):** ...

**My action:** what I kept, changed or rejected, and why.

---
-->
