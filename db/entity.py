from typing import Any, Dict, List
import local_types
from utils.settings import lazy_settings


class BaseEntityMeta(type):
    def __new__(cls, name, bases, dct):
        """
        For setting up the repository
        to entity, if repository is not set.
        This done for that, you could do something like this:
        class User(BaseEntity):
            repository = MySomeRepo()
        
        like in your lovely Django.
        """
        new_cls = super().__new__(cls, name, bases, dct)

        if not hasattr(new_cls, "repository") or not new_cls.repository:
            new_cls.repository = lazy_settings.DEFAULT_REPOSITORY(new_cls)
            return new_cls

        if isinstance(new_cls.repository, type):
            raise ValueError("Repository must be an instance, not a class.")

        new_cls.repository._init(new_cls)

        return new_cls

# Bellow comments will be boring, Cause i have tired of writing comments 0o0.

class BaseEntity(metaclass=BaseEntityMeta):
    repository: local_types.TRepository = None
    _fields: set = None

    def __init__(self, **kwargs):
        """
        Initialize the entity with given attributes.
        """
        for field, value in kwargs.items():
            self._validate_field(field)
            setattr(self, field, value)

    def save(self):
        """
        Save or update the entity in the repository.
        """
        if not self.repository:
            raise ValueError("Repository not set for this entity.")

        primary_key = lazy_settings.PRIMARY_KEY_LOOKUP
        if not hasattr(self, primary_key):
            setattr(self, primary_key, self.repository.get_next_id())

        record = self.to_dict()
        existing = self.repository.read(**{primary_key: record[primary_key]})

        if existing:
            self.repository.update({primary_key: record[primary_key]}, **record)
        else:
            self.repository.create(record)

    def delete(self):
        """
        Delete the entity from the repository.
        """
        if not self.repository:
            raise ValueError("Repository not set for this entity.")

        primary_key = lazy_settings.PRIMARY_KEY_LOOKUP
        self.repository.delete(**{primary_key: getattr(self, primary_key)})

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the entity into a dictionary.
        I'm tired & motivated wor writing docstrings. #PIP
        """
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}

    @classmethod
    def _validate_entity_fields(cls, fields: List[str]):
        """
        Validate if the fields is allowed in the entity.
        """
        if not cls._fields:
            raise AttributeError("No fields defined for %s entity." % cls.__name__)
        for field in fields:
            cls._validate_field(field)

    @classmethod
    def _validate_field(cls, field: str):
        """
        Validate if the field is allowed in the entity.
        """
        if field not in cls._fields:
            raise AttributeError(f"Invalid field {field} for {cls.__name__} entity.")
