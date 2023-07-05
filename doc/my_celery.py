from celery import Celery

app = Celery('my_celery', backend='redis://localhost', broker='redis://localhost')
CELERY_CONF = {'task_always_eager': True, }
app.conf.update(CELERY_CONF)


@app.task
def add(x, y):
    return x + y


@app.task
def xsum(*args):
    return sum(*args)


print(add(1, 1))
print(add.run(1, 2))


from celery import signature
s = signature('my_celery.add', args=(1, 2), kwargs={})
result = s.apply().get()
print(result)
result = s.delay().get()
print(result)
result = s.apply_async().get()
print(result)


from celery import chain

res = chain(add.s(1, 2), add.s(3), add.s(4), add.s(5), add.s(6), add.s(7), add.s(8))()
print(res.get())

from celery import group
res = group(add.s(i, i) for i in range(10))()
print(res.get(timeout=1))

from celery import chord
res = chord((add.s(i, i) for i in range(10)), xsum.s())()
print(res.get())
