FROM python:3.7-alpine
LABEL maintainer="Baba Sangare <sibrahima250@gmail.com>"
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/

CMD ["python", "manage.py", "runserver", "0.0.0.0:3000"]