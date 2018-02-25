from tastypie.api import Api

from api.categories import CategoriesResource
from api.entities import EntitiesDetailResource, EntitySimpleResource
from api.wallet import PaymentsResource, WalletResource
from api.resources import OffersResource, NewsResource
from api.accounts import RegisterResource, UserResource
from api.profile import EntityResource, PersonResource, DeviceResource


def get_api(version_name):

    api = Api(api_name=version_name)

    api.register(CategoriesResource())
    api.register(RegisterResource())
    api.register(UserResource())
    api.register(WalletResource())
    api.register(EntityResource())
    api.register(EntitiesDetailResource())
    api.register(EntitySimpleResource())
    api.register(OffersResource())
    api.register(PersonResource())
    api.register(PaymentsResource())
    api.register(DeviceResource())
    api.register(NewsResource())


    return api