FROM python:3.6-alpine

RUN adduser -D avitochat

WORKDIR /home/avitochat

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn pymysql

COPY app app
COPY migrations migrations
COPY chat.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP chat.py

RUN chown -R avitochat:avitochat ./
USER avitochat

EXPOSE 9000
ENTRYPOINT ["./boot.sh"]