FROM python:3.11-slim

WORKDIR /app

COPY api-devops/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY api-devops/ ./api-devops/
COPY ["Resultats-Machine Learning/", "./Resultats-Machine Learning/"]

WORKDIR /app/api-devops

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]