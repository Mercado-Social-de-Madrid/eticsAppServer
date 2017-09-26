from tastypie.api import Api

from api.resources import EntityResource, UserResource


def get_api(version_name):

    api = Api(api_name=version_name)

    api.register(EntityResource())
    api.register(UserResource())

    return api