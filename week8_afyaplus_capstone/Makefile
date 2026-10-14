install:
	pip install -r requirements.txt

check:
	ruff check --ignore E401,E701,E702,E501 .
	python check_prompt_pin.py
	pytest -q
	python eval_prompts.py
	python scripts/check_mcp_health.py

run:
	uvicorn prompt_app:app --reload
