from typing import Any, Dict

import requests
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import EmailMessage
from django.template.loader import get_template
from rest_framework_simplejwt.tokens import RefreshToken

GOOGLE_ID_TOKEN_INFO_URL = 'https://www.googleapis.com/oauth2/v3/tokeninfo'
GOOGLE_ACCESS_TOKEN_OBTAIN_URL = 'https://oauth2.googleapis.com/token'
GOOGLE_USER_INFO_URL = 'https://www.googleapis.com/oauth2/v3/userinfo'


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


def google_get_access_token(*, code: str, redirect_uri: str) -> str:
    # Reference: https://developers.google.com/identity/protocols/oauth2/web-server#obtainingaccesstokens
    data = {
        'code': code,
        'client_id': settings.GOOGLE_OAUTH2_CLIENT_ID,
        'client_secret': settings.GOOGLE_OAUTH2_CLIENT_SECRET,
        'redirect_uri': redirect_uri,
        'grant_type': 'authorization_code'
    }

    response = requests.post(GOOGLE_ACCESS_TOKEN_OBTAIN_URL, data=data)

    if not response.ok:
        raise ValidationError('Failed to obtain access token from Google.')

    access_token = response.json()['access_token']

    return access_token


def google_get_user_info(*, access_token: str) -> Dict[str, Any]:
    # Reference: https://developers.google.com/identity/protocols/oauth2/web-server#callinganapi
    response = requests.get(
        GOOGLE_USER_INFO_URL,
        params={'access_token': access_token}
    )

    if not response.ok:
        raise ValidationError('Failed to obtain user info from Google.')

    return response.json()


def generate_registration_code(name, lastRegCode):
    return f"{name[:3].upper()}-{lastRegCode+3155}"


def send_ca_confirmation_mail(instance=None):
    if instance:
        subject, to = "Welcome On Board " + str(instance.full_name) + "!", str(instance.email)
        ctx = {
            'object': instance,
        }
        body_content = get_template('ca/ca_registration_email.html').render(ctx)

        confirmation_mail = EmailMessage(subject=subject, body=body_content, to=[to])
        confirmation_mail.content_subtype = 'html'
        num_sent = confirmation_mail.send()
        if num_sent != 0:
            return True
        else:
            return False
    else:
        return False
