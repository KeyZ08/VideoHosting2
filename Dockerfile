FROM python:3.10.9

SHELL ["/bin/bash", "-c"]

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN pip install --upgrade pip

WORKDIR /site

COPY --chown=yt:yt . .

RUN pip install -r requirements.txt

CMD ["python", "manage.py", "makemigrations"]
CMD ["python", "manage.py", "migrate"]

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]