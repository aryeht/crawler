import random
import time

from crawler.adapters.cache import cache
from crawler.domain.page import page

URL_PREFIX = 'urls'
COUNTER_PREFIX = 'count'


def download_page(url: str) -> page:
    """ The function returns an instance of page object """
    time.sleep(random.randint(5, 15))
    return page(url=url, content='')


def count_word_occurrences(p: page, word: str) -> int:
    """ The function counts word occurrences in the given page """
    return random.randint(0, 100)


def get_links_in_page(p: page) -> set:
    """ The function returns set of links (strings) in the given page """
    sub_domains = ['blog', 'www', 'demo']
    domains = ['abc', 'def', 'example']
    top_level_domains = ['com', 'org', 'ai']
    return {f"https://{subd}.{d}.{tld}" for subd, d, tld in zip(sub_domains, domains, top_level_domains)}


def is_already_crawled(url: str, word: str) -> bool:
    return cache.sismember(f"{URL_PREFIX}::{word}", url)


def increment_url_word(word: str, url: str, word_count: int) -> int:
    # increment word count
    total_so_far = cache.incr(f"{COUNTER_PREFIX}::{word}", word_count)
    cache.set(f"{COUNTER_PREFIX}::{word}::{url}", word_count)
    # append URL to list of crawled urls
    cache.sadd(f"{URL_PREFIX}::{word}", url)

    return total_so_far
