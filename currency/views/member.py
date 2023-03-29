import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from helpers.pdf import render_pdf_response


def get_card_data(user_type, member):
    member_data = {
        "city": member.city.id,
        "member_id": member.member_id
    }
    card_data = {
        'user_type': user_type,
        'member_id': member.member_id,
        'display_name': member.display_name,
        'member_qr': json.dumps(member_data),
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