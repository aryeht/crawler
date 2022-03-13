from dataclasses import dataclass


@dataclass
class page:
    url: str
    content: str


@dataclass
class page_result:
    url: str
    word: str
    count: int
