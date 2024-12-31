
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
"""
* __future__: special module that allows you to use features from future Python versions in earlier versions
"""

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')

#* Use setting from django project setting
app.config_from_object('django.conf:settings', namespace='CELERY')

#* Automatically find tasks in installed_app
app.autodiscover_tasks()
