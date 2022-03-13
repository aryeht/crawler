import os

from redis import StrictRedis

CELERY_BROKER_URL = os.environ['BROKER_URL']
cache = StrictRedis.from_url(CELERY_BROKER_URL, decode_responses=True)
