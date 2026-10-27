# ATU CloudFormation Assignment: L00205332

**Module:** IaC for DevOps Pipelines, Atlantic Technological University
**Student:** _Your Name_ (L00205332)
**Lecturer:** Ruth Lennon

This README is the lab write-up for the assignment.

---

## 1. Overview

_TODO: a short summary of what the project delivers._

- **Part A(a):** a static website hosted from S3 and served publicly, with my L-number and name as the header.
- **Part A(b):** a three-tier architecture (web, application, database tiers).
- **Part B:** best practices, tooling and the "ilities" (security, scalability, performance).

## 2. Repository structure

```
.
├── templates/            # CloudFormation templates
├── website/              # Static site content uploaded to S3
├── parameters/           # Example parameter files per stack
├── .cfnlintrc.yaml       # cfn-lint configuration
├── PROMPTS.md            # Declared tutorials and LLM prompts
└── README.md             # This write-up
```

## 3. Prerequisites

- An AWS account with a non-root IAM identity (root user MFA enabled, budget alarm configured)
- AWS CLI v2 with a named profile
- [cfn-lint](https://github.com/aws-cloudformation/cfn-lint)

## 4. Part A(a): Static website on S3

### 4.1 Architecture
_TODO: diagram and description._

### 4.2 Deployment
_TODO: commands._

### 4.3 Testing
_TODO: evidence (screenshots, curl output)._

## 5. Part A(b): Three-tier architecture

### 5.1 Architecture
_TODO: diagram showing the web, app and DB tiers, subnets and security groups._

### 5.2 Deployment
_TODO_

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

_TODO: commands to delete stacks and empty buckets to avoid charges._

## 11. References

_TODO_
