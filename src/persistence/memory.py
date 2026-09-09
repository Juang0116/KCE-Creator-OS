from __future__ import annotations

from typing import Generic, TypeVar


T = TypeVar("T")


class MemoryRepository(Generic[T]):
    """
    In-memory implementation of the Repository contract.

    This implementation is intentionally simple and deterministic.
    It is used for development and testing before introducing
    external persistence infrastructure.
    """

    def __init__(self) -> None:
        self._records: dict[str, T] = {}

    def save(
        self,
        key: str,
        value: T,
    ) -> T:
        if not key:
            raise ValueError(
                "Repository key cannot be empty."
            )

        self._records[key] = value

        return value

    def get(
        self,
        key: str,
    ) -> T | None:
        return self._records.get(key)

    def exists(
        self,
        key: str,
    ) -> bool:
        return key in self._records

    def delete(
        self,
        key: str,
    ) -> bool:
        if key not in self._records:
            return False

        del self._records[key]

        return True

    def list_all(self) -> list[T]:
        return list(self._records.values())

    def clear(self) -> None:
        """
        Clear all records.

        Useful for isolated tests and local development.
        """
        self._records.clear()

    def count(self) -> int:
        """
        Return the number of stored records.
        """
        return len(self._records)