from __future__ import annotations

from typing import Generic, Protocol, TypeVar


T = TypeVar("T")


class Repository(Protocol, Generic[T]):
    """
    Generic persistence contract.

    Domain/application code depends on this interface,
    not on a concrete database implementation.
    """

    def save(
        self,
        key: str,
        value: T,
    ) -> T:
        """
        Persist or replace a value under a stable key.
        """
        ...

    def get(
        self,
        key: str,
    ) -> T | None:
        """
        Retrieve a value by key.

        Returns None when the record does not exist.
        """
        ...

    def exists(
        self,
        key: str,
    ) -> bool:
        """
        Check whether a record exists.
        """
        ...

    def delete(
        self,
        key: str,
    ) -> bool:
        """
        Delete a record.

        Returns True when a record was deleted,
        otherwise False.
        """
        ...

    def list_all(self) -> list[T]:
        """
        Return all stored values.
        """
        ...