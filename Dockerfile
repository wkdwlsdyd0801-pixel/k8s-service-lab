# Small, current base image keeps the attack surface and image size down.
FROM python:3.12-slim

# Don't buffer stdout/stderr, and don't write .pyc files: logs show up
# immediately and the layer stays clean.
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Copy only requirements first so the pip layer is cached and not rebuilt
# every time the app code changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Run as a non-root user: if the app is compromised, the attacker is not root
# inside the container. 10001 is an arbitrary high, unprivileged UID.
RUN useradd --uid 10001 --no-create-home appuser
USER 10001

EXPOSE 8080

# gunicorn is a production WSGI server; 2 workers is plenty for a demo pod.
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "2", "app:app"]
