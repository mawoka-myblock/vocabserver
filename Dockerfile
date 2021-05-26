FROM python:3.9.5-slim-buster


WORKDIR /app
COPY requirements.txt requirements.txt
RUN apt update
RUN apt install enchant hunspell hunspell-de-de hunspell-en-gb hunspell-fr -y
RUN pip3 install -r requirements.txt
COPY . .

#RUN python3 initialisation.py
CMD [ "python3", "-m" , "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
EXPOSE 80