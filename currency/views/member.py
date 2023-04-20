import urllib.parse

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse

from helpers.pdf import render_pdf_response


def get_card_data(user_type, member):
    params = f'?city={member.city.id}&member_id={member.member_id}'
    member_data_url = settings.BASESITE_URL + reverse('memeber_check') + params

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
    return render_pdf_response(request, 'member/card_pdf.html',
               card_data, filename=filename)


def member_check(request):
    return render(request, 'member/check_outside_app.html')