import requests
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from config.settings import MAILGUN_API_USERNAME, MAILGUN_API_URL, MAILGUN_API_KEY, SITE_URL
from .helpers import sign_up_confirm_account_token


def send_account_confirmation_email(user_id: int):
    user: User = User.objects.get(pk=user_id)
    from_ = f'accounts@{MAILGUN_API_USERNAME}'
    subject = 'Confirmar Creación de Cuenta'
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = sign_up_confirm_account_token.make_token(user)
    url = f"{SITE_URL}{reverse('change_password')}?uid={uid}&token={token}"
    body = render_to_string('authentication/mailing/activate_account.html', {
        'user': user,
        'uid': uid,
        'token': token,
        'url': url
    })
    response = requests.post(f'{MAILGUN_API_URL}/messages', auth=('api', MAILGUN_API_KEY), data={
        'from': from_,
        'to': user.email,
        'subject': subject,
        'html': body
    })
    return response.status_code == 200
