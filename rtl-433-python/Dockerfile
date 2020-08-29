
FROM python:3.8.5-buster

RUN pip install influxdb psutil

COPY rtl_433_influxdb_relay.py /

CMD ["python","rtl_433_influxdb_relay.py"]

