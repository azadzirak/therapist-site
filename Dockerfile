FROM python:3.13

WORKDIR /app

# COPY requirements.txt /app

COPY requirements.txt . 

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# EXPOSE 8000

RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "therapist_site.wsgi", "--bind", "0.0.0.0:8000"]
