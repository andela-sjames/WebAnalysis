FROM python:3.7.2-alpine3.8

ENV PYTHONUNBUFFERED 1

RUN apk add --no-cache lapack libstdc++

RUN apk add --no-cache --virtual build-dependencies \
    g++ \
    gcc \
    gfortran \
    musl-dev \
    lapack-dev \
    freetype-dev \
    libpng-dev \
    openblas-dev \
    && ln -s /usr/include/locale.h /usr/include/xlocale.h \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del build-dependencies

# load project files and set work directory
ADD . /app/
WORKDIR /app

CMD [ "python", "gui.py" ]
