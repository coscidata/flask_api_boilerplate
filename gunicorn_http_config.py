# -*- coding: utf-8 -*-
bind = '127.0.0.1:5000'
worker_class = 'gevent'
graceful_timeout = 3600
timeout = 3600
max_requests = 120
workers = 4
log_level = 'info'
debug = False
accesslog = '-'
errorlog = '-'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'
