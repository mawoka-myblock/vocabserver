FROM python:3.9.5-slim-buster


# Install Vocab-Server
RUN pip install --no-cache-dir "uvicorn[standard]" gunicorn

RUN mkdir /app
COPY ./start.sh /start.sh
RUN chmod +x /start.sh

COPY gunicorn_conf.py /gunicorn_conf.py

COPY ./start-reload.sh /start-reload.sh
RUN chmod +x /start-reload.sh
ENV PYTHONPATH=/app


RUN apt update
RUN apt install enchant hunspell hunspell-de-de hunspell-en-gb hunspell-fr -y
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
RUN mkdir /app/data

CMD [ "python3", "-m", "gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "main:app", "--log-level", "debug"]
EXPOSE 80