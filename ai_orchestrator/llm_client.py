import os
import time
import logging
from openai import OpenAI, RateLimitError, APIConnectionError, APITimeoutError
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

_DEFAULT_MODEL  = os.getenv("LLM_MODEL", "gpt-4")
_MAX_RETRIES    = int(os.getenv("LLM_MAX_RETRIES", "3"))
_RETRY_DELAY    = float(os.getenv("LLM_RETRY_DELAY", "2.0"))  # doubles each attempt


def call_llm(prompt: str, model: str = None, max_tokens: int = 2048) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:                    # ✅ fail fast with a clear message
        raise EnvironmentError(
            "OPENAI_API_KEY is not set. Add it to your .env file or CI secrets."
        )

    client = OpenAI(api_key=api_key)
    chosen_model = model or _DEFAULT_MODEL
    last_error = None

    for attempt in range(1, _MAX_RETRIES + 1):
        try:
            logger.info(f"[LLM] Attempt {attempt}/{_MAX_RETRIES} — model={chosen_model}")
            response = client.chat.completions.create(
                model=chosen_model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=max_tokens,
                timeout=60,            # ✅ hard timeout per call
            )
            return response.choices[0].message.content

        except RateLimitError as e:
            last_error = e
            wait = _RETRY_DELAY * (2 ** (attempt - 1))   # ✅ exponential backoff
            logger.warning(f"[LLM] Rate limit. Retrying in {wait}s...")
            time.sleep(wait)

        except (APIConnectionError, APITimeoutError) as e:
            last_error = e
            wait = _RETRY_DELAY * (2 ** (attempt - 1))
            logger.warning(f"[LLM] Connection error: {e}. Retrying in {wait}s...")
            time.sleep(wait)

        except Exception as e:
            logger.error(f"[LLM] Non-retryable error: {e}")
            raise                      # ✅ auth failures etc. fail immediately

    raise RuntimeError(
        f"LLM call failed after {_MAX_RETRIES} attempts. Last error: {last_error}"
    )


