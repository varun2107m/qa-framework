import os
import pytest
import allure
from dotenv import load_dotenv

load_dotenv()

pytest_plugins = [
    "tests.steps.common_steps",
    "tests.steps.cart_steps",
]

# Ensure artifact folders exist
for _dir in ("artifacts/trace", "artifacts/screenshots", "artifacts/html", "artifacts/logs"):
    os.makedirs(_dir, exist_ok=True)


@pytest.fixture
def page(request):
    from utils.driver_factory import get_browser
    playwright, browser, context, page = get_browser()
    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield page

    test_name = request.node.name
    trace_path = f"artifacts/trace/{test_name}.zip"
    context.tracing.stop(path=trace_path)

    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(500)

        screenshot = page.screenshot()
        allure.attach(screenshot, name="screenshot", attachment_type=allure.attachment_type.PNG)
        page.screenshot(path=f"artifacts/screenshots/{test_name}.png")

        html = page.content()
        with open(f"artifacts/html/{test_name}.html", "w") as f:
            f.write(html)
        allure.attach(html, name="page_source", attachment_type=allure.attachment_type.HTML)
        allure.attach.file(trace_path, name="trace", attachment_type=allure.attachment_type.ZIP)

    context.close()
    browser.close()
    playwright.stop()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)



