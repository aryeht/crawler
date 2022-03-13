import pytest

from crawler.domain.page import page


@pytest.fixture
def test_page():
    return page(url='test', content='test')
