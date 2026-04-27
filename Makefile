.PHONY: smoke regression all report clean docker-smoke docker-build \
        ai-story ai-pr ai-branch install

# ── Setup ─────────────────────────────────────────────────────────────────────

install:
	pip install -r requirements.txt
	playwright install --with-deps

# ── Test execution ────────────────────────────────────────────────────────────

smoke:
	python runner.py --tags=smoke --headless=true --workers=2

regression:
	python runner.py --tags=regression --headless=true --workers=2

all:
	python runner.py --headless=true --workers=4

BROWSER ?= chromium
browser:
	python runner.py --tags=smoke --browser=$(BROWSER) --headless=true

# ── Reporting ─────────────────────────────────────────────────────────────────

report:
	allure serve artifacts/allure-results

report-generate:
	allure generate artifacts/allure-results -o artifacts/allure-report --clean

# ── Docker ────────────────────────────────────────────────────────────────────

docker-build:
	docker build -t qa-framework .

docker-smoke: docker-build
	docker run --env-file .env qa-framework python runner.py --tags=smoke

# ── AI Orchestrator ───────────────────────────────────────────────────────────

STORY  ?= QA-1
PR     ?= 1
BRANCH ?= main

ai-story:
	python -m ai_orchestrator.cli --story=$(STORY)

ai-pr:
	python -m ai_orchestrator.cli --pr=$(PR)

ai-branch:
	python -m ai_orchestrator.cli --branch=$(BRANCH)

# ── Cleanup ───────────────────────────────────────────────────────────────────

clean:
	rm -rf artifacts/ ai_orchestrator/generated/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete 2>/dev/null || true
	