from db.layers.services import BaseService
from ..entities import Book
from ..repositories import BookRepository
from ..types import TBookEntity


class BookService(BaseService[TBookEntity, BookRepository]):
    def __init__(self, repository: BookRepository = None):
        super().__init__(repository=repository or BookRepository(entity_cls=Book))

    def _validate_data(self, data, partial=False):
        for field in data.keys():
            if field not in self.repository.entity_cls._fields:
                raise ValueError(
                    f"Invalid field '{field}' for model '{self.repository.entity_cls.__name__}'"
                )
