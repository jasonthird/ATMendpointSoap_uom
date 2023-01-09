FROM python:3.10

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY ./main.py /app/main.py
COPY ./clientLib.py /app/clientLib.py

CMD ["python", "main.py"]