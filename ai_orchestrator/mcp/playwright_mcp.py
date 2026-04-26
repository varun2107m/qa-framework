import subprocess


class PlaywrightMCP:

    def run_smoke_flow(self):
        result = subprocess.run(
            ["python", "runner.py", "--tags=smoke"],
            capture_output=True,
            text=True
        )

        return {
            "status": "passed" if result.returncode == 0 else "failed",
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    