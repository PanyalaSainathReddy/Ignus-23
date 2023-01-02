from django.core.mail import EmailMessage
from django.template.loader import get_template


def generate_registration_code(name, lastRegCode):
    return f"{name[:3].upper()}-{lastRegCode+3155}"


def send_ca_confirmation_mail(instance=None):
    if instance:
        subject, from_email, to = "[Ignus'23] Successfully registered as Campus Ambassador for Ignus",\
                                  'noreply@ignus.co.in', str(instance.email)
        ctx = {
            'object': instance,
        }
        body_content = get_template('ca/ca_registration_email.html').render(ctx)
        print(body_content)
        # body_content = "Hello {name},\n\nThank you for registering as a Campus Ambassador for Ignus'23. We will get back to you soon.\n\nRegards,\nTeam Ignus'23".format(name=instance.ca_user.user.first_name)
        confirmation_mail = EmailMessage(subject=subject, body=body_content, from_email=from_email, to=[to])
        confirmation_mail.content_subtype = 'html'
        num_sent = confirmation_mail.send()
        if num_sent != 0:
            return True
        else:
            return False
    else:
        return False
