import time
import functools
import os
from utils.logger import get_logger

logger = get_logger("retry")

ARTIFACT_DIR = "artifacts/screenshots"


def retry(retries=2, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None

            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logger.warning(
                        f"[{func.__name__}] Attempt {attempt}/{retries} failed: {e}"
                    )

                    # --- Screenshot + HTML dump ---
                    page = _extract_page(args, kwargs)
                    if page:
                        _save_artifacts(page, func.__name__, attempt)
                    else:
                        logger.warning(f"[{func.__name__}] Could not extract page for screenshot")

                    if attempt < retries:
                        logger.info(f"[{func.__name__}] Retrying in {delay}s...")
                        time.sleep(delay)

            raise last_exception

        return wrapper
    return decorator


def _extract_page(args, kwargs):
    """Safely extract the Playwright page object from args or kwargs."""
    try:
        return kwargs.get("page") or (
            args[0].page if args and hasattr(args[0], "page") else None
        )
    except Exception:
        return None


def _save_artifacts(page, func_name, attempt):
    """Save screenshot and HTML dump on failure."""
    try:
        os.makedirs(ARTIFACT_DIR, exist_ok=True)
        base_path = f"{ARTIFACT_DIR}/{func_name}_attempt{attempt}"

        page.screenshot(path=f"{base_path}.png")
        with open(f"{base_path}.html", "w") as f:
            f.write(page.content())

        logger.info(f"Artifacts saved: {base_path}.png / .html")
    except Exception as e:
        logger.warning(f"Failed to save artifacts: {e}")
        