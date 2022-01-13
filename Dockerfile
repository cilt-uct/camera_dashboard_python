FROM python:3.8

RUN apt-get -y update
RUN apt-get -y upgrade

COPY requirements.txt /
RUN pip3 install -r /requirements.txt
RUN pip3 uninstall -y pymongo
RUN pip3 install pymongo
#RUN apt-get update && apt-get install -y --no-install-recommends apt-utils && apt-get -y install livemedia-utils && apt -y install ffmpeg && apt-get install psmisc
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils && apt -y install ffmpeg && apt-get install psmisc

ADD ./ /camera_dashboard
WORKDIR /camera_dashboard

COPY ./docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]

EXPOSE 3000
