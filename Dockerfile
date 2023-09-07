FROM python:3.10
RUN pip install poetry

COPY . /app
WORKDIR /app

COPY pyproject.toml /app
RUN apt-get update && apt-get install git -y
RUN apt-get install -y ffmpeg

RUN poetry config virtualenvs.create false
RUN poetry install

EXPOSE 5040
ENTRYPOINT ["python"]
CMD ["app.py"]
