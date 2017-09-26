from django.contrib.auth.models import User
from tastypie import fields
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.resources import ModelResource
from tastypie.validation import FormValidation

from currency.forms.user import UserForm
from currency.models import Entity


class EntityResource(ModelResource):

    class Meta:
        queryset = Entity.objects.all()
        include_resource_uri = False
        list_allowed_methods = ['get', 'post']
        resource_name = 'entities'
        collection_name = 'entities'
        excludes = ['description', 'user']

        authentication = Authentication()
        authorization = Authorization()

    # Add thumbnail field
    def dehydrate(self, bundle):
        if bundle.obj.logo_thumbnail:
            bundle.data['logo_thumbnail'] = bundle.obj.logo_thumbnail.url
        return bundle


class UserResource(ModelResource):
    entity = fields.ToOneField(EntityResource, 'entity', null=True, full=True)

    class Meta:
        queryset = User.objects.all()
        include_resource_uri = False
        list_allowed_methods = ['get', 'post']
        resource_name = 'users'
        collection_name = 'users'
        excludes = ['password', 'is_staff', 'is_superuser' ]
        validation = FormValidation(form_class=UserForm)

        authentication = Authentication()
        authorization = Authorization()

    def obj_create(self, bundle, request=None, **kwargs):
        bundle = super(UserResource, self).obj_create(bundle, request=request, **kwargs)
        bundle.obj.set_password(bundle.data.get('password'))
        bundle.obj.save()

        return bundle