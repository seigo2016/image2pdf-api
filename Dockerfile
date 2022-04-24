FROM python:3.8

WORKDIR /app/
ENV PYTHONPATH=/app/lib/
RUN pip install "uvicorn[standard]" gunicorn
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "app:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:10090"]