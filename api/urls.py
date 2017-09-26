from tastypie.api import Api

from api.resources import EntityResource


def get_api(version_name):

    api = Api(api_name=version_name)

    api.register(EntityResource())

    return api