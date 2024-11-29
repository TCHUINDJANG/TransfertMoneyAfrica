import random
import string
from django.core.mail import send_mail
from django.conf import settings
from .models import UserRegistrationModel



def generate_otp(length=6):
    characters = string.digits
    otp = ''.join(random.choice(characters) for _ in range(length))
    return otp




def otp_send_mail(email):
    subject = 'Votre code OTP'
    otp = generate_otp()
    message = f'Votre OTP est : {otp}'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject , message , from_email , recipient_list)
    user_object = UserRegistrationModel.objects.get(email=email)
    user_object.otp = otp
    user_object.save()