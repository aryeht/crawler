import crawler.tasks


def test_crawl():
    task = crawler.tasks.crawl.s(
        'www.test.com',
        'bicycle'
    ).apply()
    assert task.status == 'SUCCESS'
