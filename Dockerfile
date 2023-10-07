FROM python:3.9-alpine3.13

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "-m", "unittest", "discover", "-s", "./src/unittest/python", "-p", "test_*.py"]

