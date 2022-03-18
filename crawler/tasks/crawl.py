from celery import group
from celery.utils.log import get_task_logger

from crawler.app import app
from crawler.service.crawl import download_page, count_word_occurrences, get_links_in_page, is_already_crawled, \
    increment_url_word

logger = get_task_logger(__name__)


@app.task(
    bind=True, name='crawl'
)
def crawl(
        self,
        url,
        word
):
    if is_already_crawled(url, word):
        logger.info("word count: url %s has already been crawled for word %s", url, word)
        return

    page = download_page(url)
    word_count = count_word_occurrences(page, word)
    links_to_crawl = get_links_in_page(page)

    logger.info("word count: %s for word %s in url %s", word_count, word, url)
    if word_count:
        total_so_far = increment_url_word(word, url, word_count)
        logger.info("word count: incremented to %s for url: %s", total_so_far, url)

    next_tasks = []
    for link in links_to_crawl:
        if link != url:
            next_task = crawl.s(link, word)
            next_tasks.append(next_task)
    return group(next_tasks)()
