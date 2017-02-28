FROM hub.c.163.com/netease_comb/ubuntu:14.04

MAINTAINER Ngerll Joe<huqiao@chinatowercom.cn>

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update
RUN apt-get -y install nginx  sed python-pip python-dev uwsgi-plugin-python
RUN apt-get -y install libxml2-dev libxslt-dev python-lxml
RUN apt-get -y install python-mysqldb

RUN sed -i s/"PermitRootLogin without-password"/"PermitRootLogin yes"/g /etc/ssh/sshd_config

copy app /var/www/app
RUN sudo pip install -r /var/www/app/requirements.txt
RUN mv /etc/nginx/nginx.conf /etc/nginx/nginx.conf.bak
copy nginx.conf /etc/nginx/nginx.conf

EXPOSE 80
EXPOSE 22

ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENTRYPOINT /usr/sbin/sshd -D

WORKDIR /var/www/app
RUN chmod 777 init.sh
ENTRYPOINT /var/www/app/init.sh
