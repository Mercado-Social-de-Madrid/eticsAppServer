import os
import re
import uuid

from django.db.models import Q
from django.utils.deconstruct import deconstructible

# Random name generator to avoid file overwrites
from fcm_django.models import FCMDevice


@deconstructible
class RandomFileName(object):
    def __init__(self, path):
        self.path = os.path.join(path, "%s%s")

    def __call__(self, _, filename):
        # @note It's up to the validators to check if it's the correct file type in name or if one even exist.
        extension = os.path.splitext(filename)[1]
        return self.path % (uuid.uuid4(), extension)


def normalize_query(query_string,
                    findterms=re.compile(r'"([^"]+)"|(\S+)').findall,
                    normspace=re.compile(r'\s{2,}').sub):

    '''
    Splits the query string in invidual keywords, getting rid of unecessary spaces and grouping quoted words together.
    Example:
    >>> normalize_query('  some random  words "with   quotes  " and   spaces')
        ['some', 'random', 'words', 'with quotes', 'and', 'spaces']
    '''

    return [normspace('', (t[0] or t[1]).strip()) for t in findterms(query_string)]

def get_query(query_string, search_fields):

    '''
    Returns a query, that is a combination of Q objects.
    That combination aims to search keywords within a model by testing the given search fields.
    '''

    query = None  # Query to search for every search term
    terms = normalize_query(query_string)

    print terms
    for term in terms:
        if len(term)<3:
            continue
        or_query = None  # Query to search for a given term in each field
        for field_name in search_fields:
            q = Q(**{"%s__icontains" % field_name: term})
            if or_query is None:
                or_query = q
            else:
                or_query = or_query | q
        if query is None:
            query = or_query
        else:
            query = query & or_query

    return query



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


from django.contrib.admin.views.decorators import user_passes_test

def superuser_required(view_func=None, login_url='dashboard'):
    """
    Decorator for views that checks that the user is logged in and is a
    superuser, redirecting to the login page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_superuser,
        login_url=login_url,
        redirect_field_name='permission'
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator