import os

from celery import Celery

CELERY_BROKER_URL = os.environ['BROKER_URL']
RESULT_BACKEND = os.environ['RESULT_BACKEND']

app = Celery(
    __name__,
    include=['tasks']
)
app.conf.update({
    'broker_url': CELERY_BROKER_URL,
    'result_backend': RESULT_BACKEND,
    'imports': (
        'tasks',
    ),
    'task_routes': {
        'crawl': {'queue': 'crawler_q'},
    },
    'task_serializer': 'json',
    'result_serializer': 'json',
    'accept_content': ['json']
})
