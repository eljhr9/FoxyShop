import os
from celery import Celery
from django.conf import settings

# set the default Django settings module for the 'celery' programm.

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_shop.settings')
#
# app = Celery('my_shop')
#
# app.config_from_object('django.conf:settings', namespace='CELERY')
# app.autodiscover_tasks()



#set the default Django settings module for the 'celery' program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_shop.settings')

app = Celery('django_shop')
app.config_from_object('django_shop.celeryconfig')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
	print('Request: {0!r}'.format(self.request))
