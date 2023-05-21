FROM python:3.10.10
WORKDIR /main project

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/

CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]