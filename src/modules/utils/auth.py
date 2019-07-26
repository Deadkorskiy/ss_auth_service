from functools import wraps
from settings import settings
from flask import request
from werkzeug.exceptions import Forbidden


def api_key_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if settings.DEBUG and settings.DISABLE_API_KEY_AUTH:
            return func(*args, **kwargs)
        api_key = str(request.headers.get('api-key', request.headers.get('API-KEY', '')))
        if api_key not in settings.API_KEYS:
            raise Forbidden()
        return func(*args, **kwargs)
    return wrapper
