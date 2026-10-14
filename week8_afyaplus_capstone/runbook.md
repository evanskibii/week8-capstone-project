# AfyaPlus Week 8 LLMOps Runbook

## Purpose
Operate versioned triage prompts and the logistics MCP service safely. The AI recommends a route; authorised clinical staff decide patient care.

## Release alignment
Use Git tag `v1.3.0`, Docker image `afyaplus-triage:v1.3.0`, app `1.3.0`, prompt `1.3.0-candidate`, and MCP `1.3.0`. Verify `python check_prompt_pin.py` and `/health` before promotion.

## Roll forward
1. Open a pull request with prompt, pin, config, golden-set, and changelog updates.
2. Obtain reviews from clinical_ops and ml-eng for clinical-adjacent prompt changes.
3. Require green `lint_test`, `eval`, and `mcp_health` checks.
4. Tag the approved commit, build the matching image tag, record its digest, and canary the candidate on 10% of staging keys.
5. Promote only if urgency agreement is at least 0.85, `check_stock` is listed and callable, and staging error rate remains below 0.10.

## Roll back
1. Set `PROMPT_VERSION=1.2.0` while retaining the same compatible image, or deploy Git tag `v1.2.0`.
2. Confirm `/health` reports the intended prompt version and SHA.
3. Re-run eval and MCP health checks, record the incident, and notify clinical_ops and ml-eng.

## Observability and evidence
CI logs and uploaded artifacts contain eval output, MCP probe output, image digest, and deploy-stub log. Application health is at `/health`. Tool counters are exposed through `tool_metrics.py`; production should export the same counters to the approved monitoring platform.

## Incident triggers
Stop or roll back on an eval score below 0.85, missing or failed `check_stock`, prompt SHA mismatch, health status not `ok`, or error rate of 0.10 or higher.

## Sprint Definition of Done
- [ ] Prompt filename, semantic version, pin SHA, config, changelog, Git tag, and image tag align.
- [ ] Golden-set labels and `must_not` constraints are reviewed by clinical_ops.
- [ ] Urgency agreement is at least 0.85 and a deliberate failing run is retained as evidence.
- [ ] MCP initializes, lists `check_stock`, and completes a safe test call.
- [ ] Pull request checks pass in the required order before build or deploy.
- [ ] Clinical-adjacent prompt changes have clinical_ops and ml-eng approval.
- [ ] No secrets or patient-identifiable data are committed.
- [ ] Roll-forward, rollback, traces, and image digest are documented.

## Governance: recommend, do not decide
AfyaPlus provides recommendations and operational support. It must not make autonomous diagnosis, treatment, admission, discharge, or emergency-denial decisions. Clinical staff retain decision authority, can override the recommendation, and should document consequential overrides. High-risk changes require human review, staged rollout, monitoring, and a tested rollback.

## Simulated retrain
`scripts/stub_retrain.py` only increments `model_version` and appends a changelog entry. It trains no weights and requires no GPU.
