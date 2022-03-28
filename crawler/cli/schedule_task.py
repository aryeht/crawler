import argparse
from datetime import datetime, timezone, timedelta

from celery.schedules import crontab
from redbeat import RedBeatSchedulerEntry as Entry

from crawler.app import app, CELERY_CONF


def delete_entry(args):
    task_name = ':'.join(['redbeat', 'cli', args.url, args.word, args.task])

    try:
        e = Entry.from_key(task_name)
    except KeyError:
        print(f"{task_name} non existing")
    else:
        e.app = app
        print('Deleting', e)
        e.delete()


def create_entry(args):
    task_name = ':'.join(['cli', args.url, args.word, args.task])

    crontab_schedule = None
    if args.when == 'asap':
        asap_utc = datetime.now(timezone.utc) + timedelta(minutes=5)
        crontab_schedule = crontab(hour=asap_utc.hour, minute=asap_utc.minute)
    else:
        if args.hour is not None and args.minute is not None:
            crontab_schedule = crontab(hour=args.hour, minute=args.minute)

    task = args.task
    entry = Entry(
        task_name,
        task,
        schedule=crontab_schedule,
        args=(args.url, args.word),
        options=CELERY_CONF['task_routes'],
        app=app,
    )
    print('New schedule', entry)
    entry.save()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest='command')
    delete = subparser.add_parser('delete')
    schedule = subparser.add_parser('schedule')

    delete.add_argument('--url', default='https://www.wikipedia.com')
    delete.add_argument('--word', default='bicycle')
    delete.add_argument('--task', default='crawl')

    schedule.add_argument('--url', default='https://www.wikipedia.com')
    schedule.add_argument('--word', default='bicycle')
    schedule.add_argument('--task', default='crawl')

    schedule.add_argument('--when')
    schedule.add_argument('--minute', type=int)
    schedule.add_argument('--hour', type=int)

    args = parser.parse_args()
    if args.command == 'schedule':
        delete_entry(args)
        create_entry(args)

    if args.command == 'delete':
        delete_entry(args)
