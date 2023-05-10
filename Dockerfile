FROM python:3.9

RUN apt-get -y update
RUN apt-get -y upgrade

COPY requirements.txt /
RUN pip3 install -r /requirements.txt
RUN pip3 uninstall -y pymongo
RUN pip3 install pymongo==3.11.2

RUN apt-get install -y --no-install-recommends apt-utils
RUN apt -y install ffmpeg
RUN apt-get install psmisc

RUN echo "deb http://www.deb-multimedia.org buster main" >> /etc/apt/sources.list
RUN apt-get update -oAcquire::AllowInsecureRepositories=true
RUN apt-get install -y --allow-unauthenticated deb-multimedia-keyring
RUN apt-get install -y --allow-unauthenticated livemedia-utils

ADD ./ /camera_dashboard
WORKDIR /camera_dashboard

COPY ./docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]

EXPOSE 3000
