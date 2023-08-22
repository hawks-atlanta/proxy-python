FROM python:alpine3.18

RUN adduser -D -u 5000 -h /opt/application -s /sbin/nologin application
WORKDIR /opt/application
COPY . .
USER application
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "-m", "flask", "-A", "./main.py", "run", "--host", "0.0.0.0", "--port", "8080"]