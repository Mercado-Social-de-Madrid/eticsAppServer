import urllib.parse

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView

from helpers.pdf import render_pdf_response


def get_card_data(user_type, member):
    params = f'?city={member.city.id}&member_id={member.member_id}'
    member_data_url = settings.BASESITE_URL + reverse('member_check') + params

    card_data = {
        'user_type': user_type,
        'member_id': member.member_id,
        'display_name': member.display_name,
        'member_qr': urllib.parse.quote(member_data_url),
    }

    if user_type == 'person':
        card_data['is_intercoop'] = member.is_intercoop
        card_data['profile_image'] = member.profile_image
    else:
        card_data['profile_image'] = member.logo

    return card_data

@login_required
def member_card(request):
    user_type, member = request.user.get_related_entity()
    card_data = get_card_data(user_type, member)
    return render(request, 'member/card.html', card_data)

@login_required
def member_card_pdf(request):
    user_type, member = request.user.get_related_entity()
    card_data = get_card_data(user_type, member)

    filename = 'carnet_mesm'
    return render_pdf_response(request, 'member/card_pdf.html', card_data, filename=filename)


class MemberCheck(TemplateView):
    template_name = 'member/check_outside_app.html'


class CheckMemberStatus(TemplateView):
    template_name = 'member/check_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['valid'] = False
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
