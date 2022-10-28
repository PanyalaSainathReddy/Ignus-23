# import random
# import string
# from django.core.mail import EmailMessage
# from django.template.loader import get_template


# def random_string_generator(size=7, chars=string.ascii_uppercase + string.digits):
#     return ''.join(random.choice(chars) for _ in range(size))


# def get_referral_code():
#     return "IG{rand_letters}{rand_digits}".format(rand_letters=random_string_generator(3, string.ascii_uppercase),
#                                                   rand_digits=random.randint(10, 99))


# def generate_registration_code(name):
#     return f"IG-{name[:3].upper()}-{random.randint(100, 999)}"


# def unique_ca_referral_code(instance, new_referral_code=None):
#     if new_referral_code is not None:
#         referral_code = new_referral_code
#     else:
#         referral_code = get_referral_code()

#     klass = instance.__class__
#     qs_exists = klass.objects.filter(referral_code=referral_code).exists()
#     if qs_exists:
#         new_referral_code = get_referral_code()
#         return unique_ca_referral_code(instance, new_referral_code=new_referral_code)
#     return referral_code


# def send_ca_confirmation_mail(instance=None):
#     if instance:
#         subject, from_email, to = "[Ignus'23] Successfully registered as Campus Ambassador for Ignus",\
#                                   'noreply@ignus.co.in', str(instance.ca_user.user.email)
#         # ctx = {
#         #     'object': instance,
#         # }
#         # body_content = get_template('registration/ca_registration_email.html').render(ctx)
#         body_content = "Hello {name},\n\nThank you for registering as a Campus Ambassador for Ignus'23. We will get back to you soon.\n\nRegards,\nTeam Ignus'23".format(name=instance.ca_user.user.first_name)
#         confirmation_mail = EmailMessage(subject=subject, body=body_content, from_email=from_email, to=[to])
#         confirmation_mail.content_subtype = 'html'
#         num_sent = confirmation_mail.send()
#         if num_sent != 0:
#             return True
#         else:
#             return False
#     else:
#         return False
