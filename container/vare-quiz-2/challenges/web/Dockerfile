FROM python:3.12-alpine
WORKDIR /app
COPY --chown=10001:10001 app.py /app/app.py
USER 10001:10001
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
EXPOSE 8080
HEALTHCHECK --interval=15s --timeout=3s --start-period=5s --retries=3 CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/',timeout=2).read()"
CMD ["python", "/app/app.py"]
