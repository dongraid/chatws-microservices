FROM python:3.9
ENV PYTHONUNBUFFERED 1
WORKDIR /app
RUN apt-get update && apt-get install -y supervisor
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app

CMD ["/usr/bin/supervisord", "-c", "supervisord.conf"]