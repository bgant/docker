
FROM python:3.9.7-buster

RUN pip install influxdb psutil

COPY rtl_433_influxdb_relay.py /

CMD ["python","/rtl_433_influxdb_relay.py"]

# Run this as a sidecar with rtl-433 container
