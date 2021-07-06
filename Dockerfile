FROM python:3.8-buster
RUN mkdir /app
WORKDIR /app
COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt
#COPY .env /app/.env
COPY getweather.py /app/

CMD ["python3", "/app/getweather.py"]
