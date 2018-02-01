from tastypie.api import Api

from api.categories import CategoriesResource
from api.entities import EntitiesResource
from api.payment import PaymentsResource
from api.resources import  OffersResource
from api.accounts import RegisterResource, UserResource
from api.profile import WalletResource, EntityResource, PersonResource, DeviceResource


def get_api(version_name):

    api = Api(api_name=version_name)

    api.register(CategoriesResource())
    api.register(RegisterResource())
    api.register(UserResource())
    api.register(WalletResource())
    api.register(EntityResource())
    api.register(EntitiesResource())
    api.register(OffersResource())
    api.register(PersonResource())
    api.register(PaymentsResource())
    api.register(DeviceResource())


    return api