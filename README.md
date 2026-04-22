# QA Automation Framework

Production-grade QA automation framework using:
Production-grade QA automation framework built with:
- Pytest for test orchestration
- Playwright for reliable UI automation
- Requests for API validation
- Layered architecture (tests → flows → pages → services)

---

## 🚀 Features

- Page Object Model (POM)
- Business Layer (Flows)
- API + UI testing
- Environment-based config
- Parallel execution
- Alure eporting
- Screenshot capture on failure


## 🧪 Data-Driven Testing

Supports:
- Faker-based dynamic data
- Deterministic data via seed
- Override support for edge cases

example:
checkout.complete_checkout(
    {
    "first_name": "Varun",
    "postal_code": "110001"
}
)

---

## 🏗️ Architecture

tests → flows → pages → utils

---

## ⚙️ Setup

```bash
git clone <repo>
cd qa-framework
pip install -r requirements.txt
pytest
