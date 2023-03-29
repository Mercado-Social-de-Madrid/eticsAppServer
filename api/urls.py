from tastypie.api import Api

from api.categories import CategoriesResource
from api.cities import CitiesResource
from api.entities import EntitiesDetailResource, EntitySimpleResource
from api.wallet import PaymentsResource, WalletResource, TransactionLogResource, SentPaymentsResource
from api.resources import OffersResource, NewsResource, BenefitResource
from api.accounts import RegisterResource, UserResource, PreRegisterResource
from api.profile import EntityResource, PersonResource, DeviceResource
from api.fetch import FetchResource
from api.members import MemberStatusResource

def get_api(version_name):

    api = Api(api_name=version_name)

    api.register(CitiesResource())
    api.register(CategoriesResource())
    api.register(RegisterResource())
    api.register(UserResource())
    api.register(TransactionLogResource())
    api.register(WalletResource())
    api.register(EntityResource())
    api.register(EntitiesDetailResource())
    api.register(EntitySimpleResource())
    api.register(OffersResource())
    api.register(PersonResource())
    api.register(PaymentsResource())
    api.register(DeviceResource())
    api.register(NewsResource())
    api.register(SentPaymentsResource())
    api.register(PreRegisterResource())
    api.register(FetchResource())
    api.register(BenefitResource())
    api.register(MemberStatusResource())

    return api