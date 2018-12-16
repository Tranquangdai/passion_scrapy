FROM tikivn/python:3.6

COPY requirements.txt ./requirements.txt
RUN pip install --upgrade --no-cache-dir pip
RUN pip install --no-cache-dir -r ./requirements.txt

RUN apt-get update && apt install -y vim && apt install unzip

ADD . "${APP_HOME}"
RUN chown -R "${APP_USER}":"${APP_GRP}" "${APP_HOME}"
