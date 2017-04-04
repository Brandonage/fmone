# Base image. A slim one for the cpu monitor
FROM python:2-alpine
# When building remember to set the context as ../../
ADD fmone /fmone

RUN apk add --no-cache --virtual .build-deps \
    gcc \
    linux-headers \
    python-dev \
    freetype-dev \
    musl-dev \
&& pip install --no-cache-dir psutil \
&& apk del .build-deps

WORKDIR /fmone

CMD python fmonitor/fmon_agent.py

