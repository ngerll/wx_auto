sudo service nginx start
gunicorn -k gevent  -b127.0.0.1:5000 index:app