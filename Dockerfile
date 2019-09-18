FROM python:3.7

COPY requirements.txt /
RUN pip3 install -r /requirements.txt
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils && apt-get -y install livemedia-utils && apt -y install ffmpeg && apt-get install psmisc

ADD ./ /camera_dashboard
WORKDIR /camera_dashboard

COPY ./docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]

EXPOSE 3000
