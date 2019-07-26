FROM python:3.6
ADD . /auth_service
WORKDIR ./auth_service
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5000
CMD [ "gunicorn", "--worker-class=gevent", "--worker-connections=1000", "--workers=3", "app", "-b", "0.0.0.0:5000"]