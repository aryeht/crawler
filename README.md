
# Project structure

## dependencies management: poetry

    poetry new crawler

access shell with:

    poetry shell

## directory structure: DDD


# Architecture: distributed tasks

Map/Reduce like implementation using Celery/Redis.


# Celery implementation 

 * Worker:
   * Crawler
 * Monitoring
   * Flower

# Results

Available in Redis:

```
127.0.0.1:6379> KEYS *
1) "count::bicycle::https://www.def.org"
2) "count::bicycle::https://blog.abc.com"
3) "_kombu.binding.celery.pidbox"
4) "count::bicycle"
5) "_kombu.binding.celeryev"
6) "_kombu.binding.crawler_q"
7) "count::bicycle::https://demo.example.ai"
8) "count::bicycle::https://www.wikipedia.com"
9) "urls::bicycle"
127.0.0.1:6379> get count::bicycle
"230"
127.0.0.1:6379> get count::bicycle::https://www.def.org
"93"
127.0.0.1:6379> get count::bicycle::https://blog.abc.com
"3"
127.0.0.1:6379> get count::bicycle::https://demo.example.ai
"98"
127.0.0.1:6379> get count::bicycle::https://www.wikipedia.com
"36"
127.0.0.1:6379> 

```