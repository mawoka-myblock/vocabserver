FROM python:3.9.5-slim-buster


WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .

#RUN python3 initialisation.py
CMD [ "python3", "-m" , "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
EXPOSE 80