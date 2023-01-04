from django.core.mail import EmailMessage
from django.template.loader import get_template


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
