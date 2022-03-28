import os

from celery import Celery

CELERY_BROKER_URL = os.environ['BROKER_URL']
RESULT_BACKEND = os.environ['RESULT_BACKEND']
SCHEDULER_URL = os.environ['SCHEDULER_URL']
TASK_TIMEOUT_S = os.environ['TASK_TIMEOUT_S']

CELERY_CONF = {
    'broker_url': CELERY_BROKER_URL,
    'result_backend': RESULT_BACKEND,
    'redbeat_redis_url': SCHEDULER_URL,
    'task_time_limit': TASK_TIMEOUT_S,
    'task_soft_time_limit': TASK_TIMEOUT_S,
    'singleton_raise_on_duplicate': True,
    'imports': (
        'tasks',
    ),
    'task_routes': {
        'crawl': {'queue': 'crawler_q'},
    },
    'task_serializer': 'json',
    'result_serializer': 'json',
    'accept_content': ['json']
}

app = Celery(
    __name__,
    include=['tasks']
)
app.conf.update(CELERY_CONF)


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # create scheduler entries as done in crawler/cli/schedule_task.py
    pass
