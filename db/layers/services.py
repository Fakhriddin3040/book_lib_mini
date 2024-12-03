from typing import Generic, List, Any, Dict
from local_types import TEntity, TRepository


class BaseService(Generic[TEntity, TRepository]):
    """"
    Base services, as any services on
    Repository, Services architecture patters.
    Nothing to comment here. Methods titles are
    answers to what they do.

    I'm !(not) tired of writing docstrings. #5
    """
    def __init__(self, repository: TRepository):
        self.repository = repository

    def create(self, **data) -> TEntity:
        self._validate_data(data)
        return self.repository.create(**data)

    def get(self, **filters) -> TEntity:
        return self.repository.get(**filters)

    def filter(self, **filters) -> List[TEntity]:
        return self.repository.filter(**filters)

    def update(self, filters: Dict[str, Any], **updates):
        self._validate_data(updates, partial=True)
        self.repository.update(filters, **updates)

    def delete(self, **filters):
        self.repository.delete(**filters)

    def all(self) -> List[TEntity]:
        return self.repository.all()

    def _validate_data(self, data: Dict[str, Any], partial: bool = False):
        """
        Validate the data before creating or updating an entity.
        Override this method in subclasses to implement custom validation logic.
        """
        pass  # By default, no validation is performed
