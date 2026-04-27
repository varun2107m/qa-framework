# QA Automation Framework

Built with Playwright · pytest-bdd · Allure · AI Orchestrator

---

## Architecture

    tests/           BDD feature files + step definitions
    flows/           Business-level reusable flows (LoginFlow, CheckoutFlow)
    pages/           Page Object Model (BasePage → LoginPage, InventoryPage …)
    services/        API client layer
    data/            DataFactory — Faker-based, seed-deterministic
    test_data/       Credential management — env-var driven
    utils/           Logger, DriverFactory, ConfigReader, Retry decorator
    ai_orchestrator/ LLM agents, MCP connectors (GitHub, Jira), CLI
    config/          YAML config per environment

---

## Quick Start

    git clone <repo>
    cd qa-framework
    make install
    cp .env.example .env
    # edit .env with your credentials
    make smoke

---

## Running Tests

    make smoke                       # smoke suite, headless, 2 workers
    make regression                  # regression suite
    make all                         # everything, 4 workers
    make browser BROWSER=firefox     # specific browser

    # or directly
    python runner.py --tags=smoke --browser=chromium --headless=true --workers=2

---

## Data-Driven Testing

    from data.data_factory import get_checkout_data

    data = get_checkout_data()                          # random
    data = get_checkout_data(seed=42)                   # deterministic
    data = get_checkout_data(overrides={"postal_code": "110001"})

---

## AI Orchestrator

Requires OPENAI_API_KEY, GITHUB_TOKEN, GITHUB_REPO in .env.

    make ai-story STORY=QA-123      # BDD + test generated from Jira story
    make ai-pr    PR=42             # AI code review — opens HTML report
    make ai-branch BRANCH=main      # AI review of entire branch

Jira story fetching requires JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN.
Without them the orchestrator runs in stub mode with a visible warning.

---

## Reporting

    make report              # serve live Allure report in browser
    make report-generate     # build static HTML report

Every test failure captures automatically:
- Screenshot (PNG)
- Full page HTML
- Playwright trace (viewable at trace.playwright.dev)

---

## Docker

    make docker-build
    make docker-smoke

    # pass secrets at runtime — never bake into image
    docker run --env-file .env qa-framework python runner.py --tags=regression

---

## Key Environment Variables

| Variable         | Description                                  |
|------------------|----------------------------------------------|
| ENV              | Target environment: qa or staging            |
| BROWSER          | chromium, firefox, or webkit                 |
| HEADLESS         | true (CI) or false (local debug)             |
| OPENAI_API_KEY   | Required for AI orchestrator                 |
| GITHUB_TOKEN     | Required for PR and branch review            |
| STANDARD_USERNAME| Falls back to standard_user if not set       |

See .env.example for the full list.


