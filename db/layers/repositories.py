from typing import Any, Dict, List
from local_types import TORM, AbstractGenericClass, TEntity
from utils.settings import lazy_settings


class BaseRepository(AbstractGenericClass[TEntity]):
    orm: TORM = None

    def __init__(self, entity_cls: TEntity = None):
        if entity_cls is not None:
            self._init(entity_cls)

    def _init(self, entity_cls: TEntity):
        """
        Initialize the repository with an ORM and a entity class.
        """
        self.entity_cls = entity_cls
        self.set_orm()

    def set_orm(self):
        """
        Set the ORM to be used by the repository.
        """
        if not hasattr(self, "orm_cls") or not self.orm_cls:
            self.orm = lazy_settings.DEFAULT_ORM(self.entity_cls.__name__.lower())
        else:
            self.orm = self.orm_cls(self.entity_cls.__name__.lower())

    def create(self, **data) -> TEntity:
        """
        Creates a new instance of the self.entity_cls and saves it to the ORM.
        I'm so tired of writing docstrings. #2
        """
        primary_key = lazy_settings.PRIMARY_KEY_LOOKUP
        if primary_key not in data:
            data[primary_key] = self.orm.get_next_id()

        self.orm.create(data)
        return self.entity_cls(**data)

    def get(self, **filters) -> TEntity:
        """
        Get a single instance matching the filters. Raises an exception if none or multiple instances are found.
        """
        results = self.orm.read(**filters)
        if len(results) == 0:
            raise ValueError("No instance found matching the given filters.")
        if len(results) > 1:
            raise ValueError("Multiple records found. Use more specific filters.")
        return self.entity_cls(**results[0])

    def filter(self, **filters) -> List[TEntity]:
        """
        Retrieve all instances matching the filters and return as entities.
        """
        results = self.orm.read(**filters)
        return [self.entity_cls(**record) for record in results]

    def update(self, filters: Dict[str, Any], **updates):
        """
        Update instances matching the filters with new data.
        """
        self.orm.update(filters, **updates)

    def delete(self, **filters):
        """
        Delete instances matching the filters.
        """
        self.orm.delete(**filters)

    def all(self) -> List[TEntity]:
        """
        Retrieve all instances in the ORM.
        I'm so tired of writing docstrings. #3
        """
        results = self.orm.read()
        return [self.entity_cls(**record) for record in results]
