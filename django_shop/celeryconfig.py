BROKER_URL = 'amqp://iqczvlmr:TnObRltMJPc97wvyK9lTIm73R64vEB-f@wasp.rmq.cloudamqp.com/iqczvlmr' #insert cloudAMQP url
BROKER_POOL_LIMIT = 1
BROKER_CONNECTION_TIMEOUT = 10
CELERYD_CONCURRENCY = 4
CELERY_RESULT_BACKEND = 'amqp://iqczvlmr:TnObRltMJPc97wvyK9lTIm73R64vEB-f@wasp.rmq.cloudamqp.com/iqczvlmr' #insert cloudAMQP url

CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT=['json']
CELERY_TIMEZONE = 'Canada/Eastern'
CELERY_ENABLE_UTC = True
