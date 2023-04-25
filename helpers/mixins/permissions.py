from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.views import View

class SuperUserCheck(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

class EntityPermissionMixin(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        type, entity = get_user_model().get_related_entity(self.request.user)
        return type is not None and type == 'entity'
