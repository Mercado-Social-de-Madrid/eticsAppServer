from tastypie.api import Api

from api.resources import EntitiesResource
from api.accounts import RegisterResource, AuthResource
from api.profile import WalletResource, EntityResource



def get_api(version_name):

    api = Api(api_name=version_name)

    api.register(EntitiesResource())
    api.register(RegisterResource())
    api.register(AuthResource())
    api.register(WalletResource())
    api.register(EntityResource())

    return api