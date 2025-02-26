import asyncio
import uuid

from collections.abc import Callable, Iterable
from functools import wraps

from django.contrib.auth.models import User

from home.models import UserProfile

from .email import send_verification_email_async


def api_user_create_verify(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args: Iterable, **kwargs: dict) -> tuple:
        result = func(*args, **kwargs)
        verification_code = str(uuid.uuid4())
        user_email = args[0].data["email"]
        UserProfile.objects.create(
            user=User.objects.get(email=user_email),
            is_verified=False,
            verification_code=verification_code
        )
        asyncio.run(send_verification_email_async(user_email, verification_code))
        return result

    return wrapper
