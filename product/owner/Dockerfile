FROM python:3

RUN mkdir -p opt/src/owner
WORKDIR /opt/src/owner/

COPY app.py ./app.py
COPY configuration.py ./configuration.py
COPY models.py ./models.py
COPY requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

ENTRYPOINT ["python", "./app.py"]

