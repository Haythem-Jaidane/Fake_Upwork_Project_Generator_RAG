FROM python:3.12.2

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

EXPOSE 8000

COPY . .

CMD ["python", "app.py"]