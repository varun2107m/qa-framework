import pytest
import os
import allure
import tests.steps.load_steps
from utils.driver_factory import get_browser

# Ensure artifact folders exist
os.makedirs("artifacts/trace", exist_ok=True)
os.makedirs("artifacts/screenshots", exist_ok=True)
os.makedirs("artifacts/html", exist_ok=True)


@pytest.fixture
def page(request):
    playwright, browser, context, page = get_browser()

    # Start tracing
    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    yield page

    # ------------------------------
    # TEARDOWN
    # ------------------------------
    test_name = request.node.name
    trace_path = f"artifacts/trace/{test_name}.zip"

    # Stop tracing
    context.tracing.stop(path=trace_path)

    # ------------------------------
    # FAILURE HANDLING
    # ------------------------------
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:

        page.wait_for_load_state("domcontentloaded")
        page.wait_for_timeout(1000)

        screenshot = page.screenshot()

        allure.attach(
            screenshot,
            name="screenshot",
            attachment_type=allure.attachment_type.PNG
        )

        page.screenshot(path=f"artifacts/screenshots/{test_name}.png")

        html = page.content()
        html_path = f"artifacts/html/{test_name}.html"

        with open(html_path, "w") as f:
            f.write(html)

        allure.attach(
            html,
            name="page_source",
            attachment_type=allure.attachment_type.HTML
        )

        allure.attach.file(
            trace_path,
            name="trace",
            attachment_type=allure.attachment_type.ZIP
        )

    # ✅ always close in order: context → browser → playwright
    context.close()
    browser.close()
    playwright.stop()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

