# Python project showcase

This project implements a dummy distributed web crawler that counts words. 
It is implemented using Map/Reduce with Celery/Redis

## Code architecture

* DDD Domain driven design
* TDD Test Driven Design

## System Architecture

* micro-service architecture
* Queue + Workers

## Monitoring

* logs
* metrics (prometheus + grafana)
* Celery Flower

## User Experience

* CLI
* Makefile

## Python

* dependency management: poetry
* type annotations
* test with `pytest` (celery tasks, service layer)

# System requirements

 * docker
 * docker compose

# Run

## Spin up all services:

   ```$ docker compose up -d```

The celery workers are then ready to pick up and process tasks.
The celery scheduler is ready to be configured and then trigger some tasks as well.

On top of the celery related containers, some extra containers are provided for:

* monitoring 
  * Celery Flower
  * Grafana
  * prometheus

* infrastructure
  * Redis: used as a broker for celery as well as it's result backend
  * nginx: used as a reverse proxy to access:
   
 |service| URL|
 |-------|----|
 |flower|http://localhost/flower|
 |grafana|http://localhost|


## Trigger some tasks

```$ docker compose exec crawler python cli/crawl.py```

## Schedule a task ASAP

```docker compose exec crawler python cli/schedule_task.py schedule --when asap```

## Run all commands above at once

In order to quickly run all commands above, a Makefile is available with the `rebuild` target

   ```$ make rebuild```

The word count is then available in Redis.


## run tests

   ```$ make tests```


# Project structure

## dependencies management: poetry

    poetry new crawler

access shell with:

    poetry shell

## directory structure: DDD

### Adapter pattern: Redis

### Service Layer: Dummy crawler

### Domain objects: Page, Page Results


# Architecture: distributed tasks

Map/Reduce like implementation using Celery/Redis.


# Results

Available in Redis:

```
$ redis-cli
127.0.0.1:6379> KEYS count::*
1) "count::bicycle::https://demo.example.ai"
2) "count::bicycle"
3) "count::bicycle::https://www.def.org"
4) "count::bicycle::https://www.wikipedia.com"
5) "count::bicycle::https://blog.abc.com"
127.0.0.1:6379> GET count::bicycle
"221"
127.0.0.1:6379> 

```