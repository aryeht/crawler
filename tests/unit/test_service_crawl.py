def test_get_links_in_page(test_page):
    from crawler.service.crawl import get_links_in_page
    links = get_links_in_page(test_page)
    assert links
