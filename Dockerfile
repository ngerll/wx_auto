FROM index.tenxcloud.com/tenxcloud/ubuntu

MAINTAINER Ngerll Joe<huqiao@chinatowercom.cn>

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get -y install nginx  sed python-pip python-dev uwsgi-plugin-python
RUN apt-get -y install libxml2-dev libxslt-dev python-lxml
RUN apt-get -y install python-mysqldb

copy app /var/www/app
RUN sudo pip install -r /var/www/app/requirements.txt
RUN mv /etc/nginx/nginx.conf /etc/nginx/nginx.conf.bak
copy nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /var/www/app
RUN chmod 777 init.sh
ENTRYPOINT /var/www/app/init.sh
