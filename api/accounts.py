from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from tastypie import fields
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.models import ApiKey
from tastypie.resources import ModelResource
from tastypie.validation import FormValidation

from currency.forms.user import UserForm


class RegisterResource(ModelResource):
    entity = fields.ToOneField('api.resources.EntityResource', 'entity', null=True, full=True)

    class Meta:
        queryset = User.objects.all()
        include_resource_uri = False
        always_return_data = True
        list_allowed_methods = ['post']
        resource_name = 'register'
        excludes = ['password', 'is_staff', 'is_superuser' ]
        validation = FormValidation(form_class=UserForm)

        authentication = Authentication() # No need for auth, public resource
        authorization = Authorization()

    def hydrate(self, bundle):

        if ('email' in bundle.data and bundle.data.get('email') != '')\
                and 'entity' in bundle.data and not ('email' in bundle.data['entity']):
            bundle.data['entity']['email'] = bundle.data['email']

        return bundle

    def obj_create(self, bundle, request=None, **kwargs):
        bundle = super(RegisterResource, self).obj_create(bundle, request=request, **kwargs)
        user = bundle.obj
        password = bundle.data.get('password')

        user.set_password(password)
        user.save()

        u = authenticate(username=user.username, password=password)
        if u is not None and u.is_active:
            login(bundle.request, u)

        return bundle


    def dehydrate(self, bundle):

        key = ApiKey.objects.get_or_create(user=bundle.obj)[0].key
        bundle.data = { 'api_key': key }
        if bundle.obj.entity:
            bundle.data['entity'] = bundle.obj.entity.pk

        return bundle