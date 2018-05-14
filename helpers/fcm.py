from django.contrib.auth.models import User
from fcm_django.models import FCMDevice


def notify_user(user, data, title=None, message=None, silent=True):
    '''
        Sends an FCM notification to a user
        If the message is silent, title and message are included in the data dictionary
    '''

    if not user:
        return

    if not data:
        data = {}
    if not message and not title:
        silent = True
    if title and silent:
        data['title'] = title
    if message and silent:
        data['message'] = message

    device = FCMDevice.objects.filter(user=user, active=True).first()
    if device is None:
        return
    if silent:
        result = device.send_message(data=data)
    else:
        kwargs = {
            'extra_kwargs': {
                'mutable_content': True,
            }
        }
        result = device.send_message(title=title, body=message, data=data, time_to_live=30, content_available=True, sound='default', **kwargs)
    return result



def broadcast_notification(users=None, data=None, title=None, body=None, silent=True):
    '''
        Sends an FCM notification to a user
        If the message is silent, title and message are included in the data dictionary
    '''

    devices = FCMDevice.objects.all()
    if users is not None:
        devices.filter(user__in=users, active=True)

    if not data:
        data = {}
    if not body and not title:
        silent = True
    if title and silent:
        data['title'] = title
    if body and silent:
        data['message'] = body

    if silent:
        result = devices.send_message(data=data)
    else:
        kwargs = {
            'extra_kwargs': {
                'mutable_content': True,
            }
        }
        result = devices.send_message(title=title, body=body, data=data, time_to_live=30, content_available=True, sound='default', **kwargs)

    return result