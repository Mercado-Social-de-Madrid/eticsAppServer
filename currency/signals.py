from django.contrib.auth.models import User
from django.db.models import signals
from tastypie.models import create_api_key

signals.post_save.connect(create_api_key, sender=User)