from tastypie.api import Api

from api.resources import EntityResource, RegisterResource


def get_api(version_name):

    api = Api(api_name=version_name)

    api.register(EntityResource())
    api.register(RegisterResource())

    return api