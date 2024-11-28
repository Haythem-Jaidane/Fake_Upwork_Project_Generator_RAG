FROM python:3.10-alpine

WORKDIR /

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

EXPOSE 8000

COPY . .

CMD ["python", "app.py"]