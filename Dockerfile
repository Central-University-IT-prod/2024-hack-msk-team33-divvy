FROM python:3.12-slim


WORKDIR /app

COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8011

CMD ["uvicorn", "web_app.run:app", "--host=0.0.0.0", "--port=8011"]
