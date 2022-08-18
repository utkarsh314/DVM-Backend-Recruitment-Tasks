FROM python:latest

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

COPY socialmedia/requirements.txt .
RUN pip install -r requirements.txt

COPY ./socialmedia /socialmedia

WORKDIR /socialmedia

COPY ./entrypoint.sh /

ENTRYPOINT ["sh", "/entrypoint.sh"]