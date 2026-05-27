from dataclasses import dataclass, field


@dataclass
class BookNode:
    isbn: str
    title: str
    author: str
    publisher: str
    pub_year: str
    genre: str
    loan_count: int = 0
    keywords: list = field(default_factory=list)
