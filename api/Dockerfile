FROM python:3.6
LABEL maintainer "Joseph Farrell <joe@joefarrell.dev>"

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY *.py /app
RUN chmod a+x *.py

CMD ["./main.py"]
