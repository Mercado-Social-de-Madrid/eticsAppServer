from fcm_django.models import FCMDevice


def notify_user(user, data, title=None, message=None, silent=True):
    '''
        Sends an FCM notification to a user
        If the message is silent, title and message are included in the data dictionary
    '''

    device = FCMDevice.objects.filter(user=user).first()
    if device is None:
        return

    if not data:
        data = {}
    if not message and not title:
        silent = True
    if title and silent:
        data['title'] = title
    if message and silent:
        data['message'] = message

    result = device.send_message(title, message, data=data)
    print result