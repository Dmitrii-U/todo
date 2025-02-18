from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse


def send_verification_email(user_email: str, verify_code: str) -> None:
    params = {
        "recipient_list": [user_email],
        "subject": "Подтверждение регистрации",
        "from_email": settings.DEFAULT_FROM_EMAIL,
    }
    relative_url = reverse('user_verify', args=[verify_code])
    url = f"{settings.SITE_URL}{relative_url}"
    message = f"Для подтверждения регистрации перейдите по ссылке: {url}"
    params["message"] = message
    send_mail(**params)


def send_recovery_email(user_email: str, verification_code: str) -> None:
    params = {
        "recipient_list": [user_email],
        "subject": "Восстановление пароля",
        "from_email": settings.DEFAULT_FROM_EMAIL,
    }
    message = f"Код для смены пароля: {verification_code}"
    params["message"] = message
    send_mail(**params)
