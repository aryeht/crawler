---
theme: gaia
_class: lead
paginate: true
backgroundColor: #fff

[comment]: <> (backgroundImage: url&#40;'https://docs.celeryq.dev/en/stable/_static/celery_512.png;)
---

# Celery tasks orchestration


![bg left:20% 40%](https://docs.celeryq.dev/en/stable/_static/celery_512.png)

---
# Celery Intro 1
 
## use case: async task executed in the background

Example: web API can offload CPU intensive tasks to workers and return immediately

---
# Celery Intro 2

# use case: orchestrate distributed tasks

Similar to Airflow 

---

# Celery Intro 3 - batteries included -

* easy configuration of task routes (which queue)
* build in scheduler or better `celery-redbeat` (dynamic)
* task runtime limits (soft and hard timeouts)
* support for retries
* Singleton (locks)
* nice admin UI: Flower
* test tasks eagerly (in the same process as the test suite)
* resource leak protection `--max-tasks-per-child`

--- 
# Celery Intro 4  - what does it need 1/2?

## broker / transport
* **Redis**
* RabbitMQ
* amazon SQS

--- 
# Celery Intro 4  - what does it need 2/2?

## results backend: store task state(SUCCESS, FAILURE...) + result

* **Redis**
* ~~RabbitMQ~~
* memcached
* SQLAlchemy, Django ORM
* Cassandra, Elasticsearch...

https://docs.celeryq.dev/en/stable/getting-started/introduction.html#transports-and-backends

--- 

# Celery Intro 5 - how does it work (signatures)?

It needs to serialize whatever is necessary to execute a function: name + arguments 

```my_celery.py
# file name: my_celery.py
from celery import Celery

app = Celery('my_celery', backend='redis://localhost', broker='redis://localhost')
CELERY_CONF = {'task_always_eager': True, }
app.conf.update(CELERY_CONF)

@app.task
def add(x, y):
    return x + y

print(add(1, 1))

from celery import signature
s = signature('my_celery.add', args=(1, 2), kwargs={})
result = s.apply().get()
print(result)
```
--- 

# Celery Intro 6 - how does it work (concurrency)?

 ## concurrency
* Prefork
* Eventlet, gevent
* Single threaded (solo)
---

# Celery Intro 7 - how does it work (serialization)?

 ## Serialization

 * ~~pickle~~, **json**, yaml, msgpack
 * zlib, bzip2 compression
 * Cryptographic message signing

---

# task orchestration

In order to be orchestrated with ease tasks should be:

 * Atomic 
 * Idempotent
 * Composable (self contained + stateless)

---

# task orchestration  - primitives

## chain

## group

## chord

## and also: map, starmap, chunk see [celery canvas](https://docs.celeryproject.org/en/stable/userguide/canvas.html)

---

# task orchestration  - chain example

> The chain primitive lets us link together signatures so that one is called after the other, essentially forming a chain of callbacks.

the output of the previous task in the chain is used as the input of the next

```
from celery import chain

res = chain(add.s(1, 2), add.s(3), add.s(4), add.s(5), add.s(6), add.s(7), add.s(8))()
print(res.get())
# 36
```

---

# task orchestration  - group example 1

> The group primitive is a signature that takes a list of tasks that should be applied in parallel.

tasks in a group as executed in parallel depending on the number of available workers

```
from celery import group
res = group(add.s(i, i) for i in range(10))()
print(res.get(timeout=1))
# [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
```
---

# task orchestration  - group  example 2 

from provided word count

```
    next_tasks = []
    for link in links_to_crawl:
        if link != url:
            next_task = crawl.s(link, word)
            next_tasks.append(next_task)
    return group(next_tasks)()
```
---

# task orchestration  - chord

essentially group + callback

>The chord primitive enables us to add a callback to be called when all of the tasks in a group have finished executing. This is often required for algorithms that aren’t embarrassingly parallel:

---

# task orchestration  - chord example 1
```
@app.task
def xsum(*args):
    return sum(*args)

from celery import chord
res = chord((add.s(i, i) for i in range(10)), xsum.s())()
print(res.get())
# 90
```
---

# task orchestration  - chord example 2

ETL implemented with a data lake architecture

Ingestion of `transactions`: **main_ingest_task**
Ingestion of `transactionlines`, `transactionaccountinglines` with the same transaction IDs: **group(tables_group)**

When the above is written in S3, the callback of the chord inserts the data in our DB (data warehouse) **s3_group_to_db.s(group_name)**

```
        # Chaining a group together with another task will automatically upgrade it to be a chord:
        single_chord = chain(main_ingest_task, group(tables_group), s3_group_to_db.s(group_name))
```

--- 

# Example + demo

https://github.com/aryeht/crawler
implementation of Map/Reduce using Celery/Redis for a word count

---

# References

 * https://celery-workflows.herokuapp.com/#/ and https://www.youtube.com/watch?v=XoMu8vhdc-A
 * https://www.distributedpython.com/
 * https://testdriven.io/blog/flower-nginx/
 * https://www.python-celery.com/2018/05/29/task-routing/.
 * https://tomwojcik.com/posts/2021-03-02/testing-celery-without-eager-tasks

---

Thanks Tikal + Fintastic

presentation created with MARP
