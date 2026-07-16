# Official Playwright image ships browsers + OS deps matching the pip version.
FROM mcr.microsoft.com/playwright/python:v1.55.0-noble

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && playwright install chromium

COPY bot.py .

# One-shot bot; term can be overridden as a command argument.
ENTRYPOINT ["python", "bot.py"]
