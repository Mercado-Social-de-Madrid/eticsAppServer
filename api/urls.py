from tastypie.api import Api

from api.profile import WalletResource
from api.resources import EntityResource, RegisterResource, AuthResource


def get_api(version_name):

    api = Api(api_name=version_name)

    api.register(EntityResource())
    api.register(RegisterResource())
    api.register(AuthResource())
    api.register(WalletResource())
    api.register(EntityResource())

    return api