FROM python:3.8-slim-bullseye
LABEL authors="auosun"

ENV LANG="C.UTF-8" \
    TERM="xterm" \
    TZ="Asia/Shanghai" \
    PUID=0 \
    PGID=0 \
    UMASK=000 \
    DEBUG=false \
    PORT=3000

WORKDIR "/app"
COPY . .
RUN pip install --upgrade pip \
    && pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip install -r requirements.txt

EXPOSE 3000
CMD ["python", "./app.py"]
