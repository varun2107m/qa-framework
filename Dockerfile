FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN playwright install --with-deps

COPY . .

# ✅ non-secret defaults — safe to bake into image
ENV ENV=qa \
    BROWSER=chromium \
    HEADLESS=true \
    WORKERS=2 \
    LOG_LEVEL=INFO

# Secret env vars must be passed at runtime — never bake into image:
#
#   docker run --env-file .env qa-framework
#   docker run -e OPENAI_API_KEY=sk-... -e GITHUB_TOKEN=ghp_... qa-framework

CMD ["python", "runner.py", "--workers=2", "--headless=true"]
