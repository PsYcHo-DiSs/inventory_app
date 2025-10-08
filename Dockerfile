FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN if [ ! -d "alembic" ]; then \
        alembic init alembic && \
        alembic revision --autogenerate -m "initial" && \
        echo "✅ Generated initial migration"; \
    fi

ENV PYTHONPATH=app/src
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV=production

EXPOSE 5000

CMD ["sh", "-c", "alembic upgrade head && python -m src.app"]