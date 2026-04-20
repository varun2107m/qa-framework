import argparse
import pytest
import os
import sys
from dotenv import load_dotenv

load_dotenv()


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--env", default=os.getenv("ENV", "qa"))
    parser.add_argument("--browser", default=os.getenv("BROWSER", "chromium"))
    parser.add_argument("--headless", default=os.getenv("HEADLESS", "false"))
    parser.add_argument("--workers", default=os.getenv("WORKERS", "1"))
    parser.add_argument("--tags", default=os.getenv("TAGS", ""))

    args = parser.parse_args()

    os.environ["ENV"] = args.env
    os.environ["BROWSER"] = args.browser
    os.environ["HEADLESS"] = args.headless
    os.environ["WORKERS"] = args.workers

    pytest_args = []

    # Tag filtering
    if args.tags:
        pytest_args.extend(["-m", args.tags])

    # Parallel execution
    if args.workers != "1":
        pytest_args.extend(["-n", args.workers])

    # Allure results
    os.makedirs("artifacts/allure-results", exist_ok=True)
    pytest_args.append("--alluredir=artifacts/allure-results")

    # Verbose output
    pytest_args.append("-v")

    # ✅ Exit with pytest's exit code so CI/CD pipelines detect failures
    sys.exit(pytest.main(pytest_args))


if __name__ == "__main__":
    main()
    



