FROM python:3.7.3-alpine

WORKDIR /webanalysis

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "gui.py" ]
