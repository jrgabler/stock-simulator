FROM python:3.6
LABEL maintainer "Joseph Farrell <joe@joefarrell.dev>"

EXPOSE 5000

WORKDIR /app/

COPY requirements.txt .
RUN pip install -r ./requirements.txt

COPY ./main.py .
COPY ./api ./api
COPY ./controllers ./controllers
COPY ./models ./models
COPY ./Resources ./Resources
COPY ./view ./view
COPY ./views ./views

CMD ["python", "./main.py"]
