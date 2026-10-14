# Change-control brief for clinical_ops

## What changed
The triage wording moves from prompt 1.2.0 to 1.3.0-candidate for 10% of staging keys. The candidate makes emergency warning patterns explicit and keeps the service advisory rather than diagnostic.

## What was tested
CI checks labelled cases in `evals/golden.jsonl`, including expected urgency and outcomes the system must not produce. The pipeline prints `eval_score` and blocks release below 0.85. It also checks that the logistics service starts, lists `check_stock`, and completes a test call.

## Rollback
Set `PROMPT_VERSION=1.2.0` with the same compatible image, or redeploy Git tag `v1.2.0`. Confirm the selected version and SHA on `/health`.

## Approval
The pull request must be approved by clinical_ops and ml-eng through CODEOWNERS. Replace `PR #__` with the submitted pull-request number.

## Go or no-go
**Go** only when eval is green, the MCP handshake lists and calls `check_stock`, the prompt pin matches, and staging error rate stays below 0.10. Otherwise **no-go** and roll back.

## What this means for teams
The system recommends a triage route. It does not diagnose or replace clinical judgement. Clinical staff remain responsible for care decisions and may stop the rollout if behaviour appears unsafe.
