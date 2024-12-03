from typing import TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from .entities import Book

TBookEntity = TypeVar("TBookEntity", bound="Book")
