from django.core.mail import send_mail
from django.template.loader import render_to_string


def send_template_email(title, destination, template_name, template_params):

    msg_plain = render_to_string('email/%s.txt' % template_name, template_params)
    msg_html = render_to_string('email/%s.html' % template_name, template_params)

    print msg_html
    print msg_plain

    send_mail(
        title,
        msg_plain,
        'noreply@mercadosocial.net',
        [destination],
        html_message=msg_html,
    )