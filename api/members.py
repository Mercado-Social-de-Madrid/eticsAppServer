from django.conf.urls import url
from tastypie import fields
from tastypie.authentication import Authentication, ApiKeyAuthentication
from tastypie.authorization import Authorization
from tastypie.http import HttpUnauthorized, HttpBadRequest, HttpNotFound
from tastypie.resources import ModelResource, Resource

from benefits.models import Benefit
from currency.models import Person, Entity
from news.models import News
from offers.models import Offer


class MemberStatusResource(Resource):

    class Meta:
        queryset = Person.objects.all()
        include_resource_uri = False
        list_allowed_methods = ['get']
        resource_name = 'member_status'
        excludes = []
        authentication = Authentication()
        authorization = Authorization()


    def prepend_urls(self):
        return [
            url(r"^member_status/$", self.wrap_view('check_status'), name='api_member_status'),
        ]

    def check_status(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        city = request.GET.get('city', None)
        member_id = request.GET.get('member_id', None)

        if not city or not member_id:
            return HttpBadRequest()

        response = {
            'city': city,
        }
        member = Person.objects.filter(city=city, member_id=member_id).first()
        if member is not None:
            response['member_type'] = 'person'
            response['is_intercoop'] = member.is_intercoop
            response['is_guest_account'] = member.is_guest_account
        else:
            member = Entity.objects.filter(city=city, member_id=member_id).first()
            if member is None:
                return HttpNotFound()
            response['member_type'] = 'entity'
        response['is_active'] = not member.inactive

        return self.create_response(request, response)

