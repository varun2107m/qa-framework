import os
import time
import logging
import requests


logger = logging.getLogger(__name__)


class JiraMCP:
    """
    Jira MCP Client

    Required env vars:
        JIRA_BASE_URL    e.g. https://yourorg.atlassian.net
        JIRA_EMAIL       your Atlassian account email
        JIRA_API_TOKEN   from id.atlassian.com/manage-profile/security/api-tokens

    Optional env vars:
        JIRA_MAX_RETRIES (default: 3)
        JIRA_RETRY_DELAY (default: 2 seconds)
    """

    def __init__(self):
        self.base_url = os.getenv("JIRA_BASE_URL", "").rstrip("/")
        self.email = os.getenv("JIRA_EMAIL", "")
        self.token = os.getenv("JIRA_API_TOKEN", "")

        self.max_retries = int(os.getenv("JIRA_MAX_RETRIES", 3))
        self.retry_delay = float(os.getenv("JIRA_RETRY_DELAY", 2))

        self._configured = bool(self.base_url and self.email and self.token)

    def get_story(self, story_id: str) -> dict:
        if not self._configured:
            import warnings
            warnings.warn(
                "JiraMCP is in STUB mode — set JIRA_BASE_URL, JIRA_EMAIL, "
                "JIRA_API_TOKEN to connect to a real Jira instance.",
                UserWarning,
                stacklevel=2,
            )
            return {
                "id": story_id,
                "title": f"[STUB] Story {story_id}",
                "description": "Stub data — configure Jira env vars for real stories.",
                "status": "STUB",
                "assignee": "N/A",
            }

        url = f"{self.base_url}/rest/api/3/issue/{story_id}"

        logger.info(f"Fetching Jira story: {story_id}")

        for attempt in range(1, self.max_retries + 1):
            try:
                response = requests.get(
                    url,
                    auth=(self.email, self.token),
                    headers={"Accept": "application/json"},
                    timeout=10,
                )

                response.raise_for_status()
                data = response.json()
                fields = data.get("fields", {})

                return {
                    "id": story_id,
                    "title": fields.get("summary", story_id),
                    "description": _extract_adf_text(fields.get("description")),
                    "status": (fields.get("status") or {}).get("name", "Unknown"),
                    "assignee": (fields.get("assignee") or {}).get("displayName", "Unassigned"),
                }

            except requests.exceptions.RequestException as e:
                logger.warning(
                    f"Attempt {attempt}/{self.max_retries} failed for {story_id}: {e}"
                )

                if attempt == self.max_retries:
                    logger.error(f"Jira API failed after retries for {story_id}")

                    return {
                        "id": story_id,
                        "title": f"[ERROR] {story_id}",
                        "description": f"Failed to fetch from Jira: {str(e)}",
                        "status": "ERROR",
                        "assignee": "N/A",
                    }

                sleep_time = self.retry_delay * (2 ** (attempt - 1))
                time.sleep(sleep_time)


def _extract_adf_text(adf) -> str:
    """
    Recursively extract plain text from Atlassian Document Format (ADF).
    Handles dicts, lists, and nested structures safely.
    """
    if not adf:
        return ""

    if isinstance(adf, dict):
        if adf.get("type") == "text":
            return adf.get("text", "")

        text_parts = []
        for child in adf.get("content", []):
            text_parts.append(_extract_adf_text(child))

        return " ".join(filter(None, text_parts)).strip()

    if isinstance(adf, list):
        return " ".join(_extract_adf_text(item) for item in adf)

    return ""


    