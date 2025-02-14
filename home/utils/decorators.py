import uuid

from collections.abc import Callable, Iterable
from functools import wraps

from django.contrib.auth.models import User

from home.models import UserProfile

from .email import send_verification_email


def api_user_create_verify(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args: Iterable, **kwargs: dict) -> tuple:
        result = func(*args, **kwargs)
        verify_code = str(uuid.uuid4())
        user_email = args[0].data["email"]
        UserProfile.objects.create(
            user=User.objects.get(email=user_email),
            is_verified=False,
            verify_code=verify_code
        )
        send_verification_email(user_email, verify_code)
        return result

    return wrapper
