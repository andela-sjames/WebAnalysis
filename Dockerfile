FROM python:3.7.2-alpine3.8

ENV PYTHONUNBUFFERED 1

RUN apk add --no-cache \
    freetype-dev \
    lapack \
    libpng-dev \
    libstdc++ \
    tcl \
    tk

ADD requirements.txt .
RUN apk add --no-cache --virtual build-dependencies \
    g++ \
    gcc \
    gfortran \
    lapack-dev \
    musl-dev \
    && ln -s /usr/include/locale.h /usr/include/xlocale.h \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del build-dependencies

# load project files and set work directory
ADD . /app/
WORKDIR /app

RUN addgroup -S docker && adduser -S docker -D docker
USER docker

CMD [ "python", "gui.py" ]
