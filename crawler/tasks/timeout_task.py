from functools import wraps
from celery.exceptions import SoftTimeLimitExceeded


def timeout_task(func):
    @wraps(func)
    def _wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SoftTimeLimitExceeded:
            raise
    return _wrapper
