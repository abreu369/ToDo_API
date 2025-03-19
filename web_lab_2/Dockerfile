FROM python:3

WORKDIR /app

COPY requirements.txt .
COPY ./entrypoint.sh /entrypoint.sh


RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x /entrypoint.sh

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
