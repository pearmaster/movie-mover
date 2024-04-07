FROM python:3.12-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN mkdir -p /usr/local/app
WORKDIR /usr/local/app

COPY pyproject.toml README.md ./
RUN pip install .

COPY classifier ./

ENTRYPOINT ["python", "sort_movies.py"]