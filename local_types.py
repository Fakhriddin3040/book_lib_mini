from typing import Generic, TypeVar, TYPE_CHECKING
from abc import ABC

"""
Generic type variables
"""

if TYPE_CHECKING:
    from db.entity import BaseEntity
    from db.orm import MacroFileORM
    from db.layers.repositories import BaseRepository

T = TypeVar("T")
TEntity = TypeVar("TEntity", bound="BaseEntity")
TORM = TypeVar("TORM", bound="MacroFileORM")
TRepository = TypeVar("TRepository", bound="BaseRepository")


class AbstractGenericClass(ABC, Generic[T]):
    pass
