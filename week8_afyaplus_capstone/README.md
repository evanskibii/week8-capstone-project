# Week 8, CI/CD for Versioned AI + MCP Health

## Overview
This repository versions AfyaPlus triage prompts, runtime configuration, a deterministic model fixture, and a logistics MCP server. Pull requests and main-branch changes pass lint/tests, a fail-closed golden-set regression gate, and an MCP handshake/tool-call probe before an image can be built. `/health` exposes the exact prompt SHA and aligned runtime versions.

## Versions
- prompts: `1.2.0` baseline and `1.3.0-candidate` pinned at `9f812975f56898c54bf995f6c5e233b962d8d6a03628f89330973a7857abd738`
- config/model_version: `stub-triage-1.0.0`
- app and MCP server: `1.3.0`
- release and image tag: `v1.3.0` and `afyaplus-triage:v1.3.0`

## Local setup
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python check_prompt_pin.py
pytest -q
python eval_prompts.py
python scripts/check_mcp_health.py
uvicorn prompt_app:app --reload
```
Open `http://127.0.0.1:8000/health` and API docs at `http://127.0.0.1:8000/docs`.

## Pipeline
GitHub Actions is in `.github/workflows/ci.yml`; the equivalent Azure DevOps definition is `azure-pipelines.yml`. Required order: `lint_test -> eval -> mcp_health -> build_deploy_stub`. Pull requests stop before deploy; main, tags, and manual dispatch can reach the build/deploy stub after all gates pass.

For a local GitHub Actions run with `act`: `act workflow_dispatch`. If `act` is unavailable, run the commands in `Makefile` and retain console output in `evidence/`.

## Eval gate
Metric: urgency agreement. Threshold: `0.85`. Dataset: `evals/golden.jsonl`. Normal run: `python eval_prompts.py`. Deliberate failure evidence: `python eval_prompts.py --force-failure`; the command returns exit code 1 and blocks the next stage.

## MCP health
Run `python scripts/check_mcp_health.py`. The probe starts the local stdio MCP stub, sends `initialize`, asserts server version `1.3.0`, lists tools, requires `check_stock`, calls it, and exits non-zero on any failure. Demonstrate fail-closed behaviour with `python scripts/check_mcp_health.py --expect-tool missing_tool`.

## Docker and deployment fallback
```powershell
docker build -t afyaplus-triage:v1.3.0 .
docker compose up -d
curl http://127.0.0.1:8000/health
docker image inspect afyaplus-triage:v1.3.0 --format='{{.Id}}'
```
The pipeline records the digest and ends with a deploy stub, so no Kubernetes or paid cloud account is required.

## Runbook and Definition of Done
See `runbook.md` for roll-forward, rollback, traces, reviewers, the sprint Definition of Done, and the recommend-against-decide governance note. The plain-language stakeholder note is `clinical_ops_change_brief.md`.

## Fallbacks declared
- [x] `act`, `workflow_dispatch`, or local dry run when Actions minutes are unavailable
- [x] stub retrain that changes only `model_version`; no weights are trained
- [x] local stdio MCP server and fail-closed health probe
- [x] stubbed model outputs; no paid OpenAI or Azure service
- [x] local Docker build and deploy stub; no Kubernetes required

## Evidence commands
```powershell
python eval_prompts.py *> evidence/eval-pass.log
python eval_prompts.py --force-failure *> evidence/eval-fail.log
python scripts/check_mcp_health.py *> evidence/mcp-pass.log
python scripts/check_mcp_health.py --expect-tool missing_tool *> evidence/mcp-fail.log
```
The two deliberate failure commands must return non-zero. Commit the resulting non-sensitive logs or attach them to the submission together with the CI run link.

## Weeks 6 and 7 reuse
The FastAPI triage shape, MCP-aware `check_stock` tool, Docker tagging, cost-free stub model, health endpoint, and observability counter pattern are carried forward. Week 8 adds semantic versions, prompt SHA pinning, CI sequencing, regression enforcement, MCP health enforcement, release evidence, and rollback documentation.

## NCA-GENL mapping
- Versioned artefacts and pipeline: deployment and operational capability
- Golden-set gate: evaluation and model assessment
- MCP health: architecture and integration
- Runbook and clinical brief: communication and stakeholder objective

## Submission checklist
- [x] Tag alignment documented
- [x] Eval fails closed
- [x] MCP health runs before build/deploy
- [x] Runbook, Definition of Done, governance note, and clinical brief included
- [x] Weeks 6 and 7 reuse documented
- [x] `.env` excluded and no secrets required
- [ ] Add actual CI link, PR number, screenshots/logs, and create Git tag `v1.3.0` after pushing
