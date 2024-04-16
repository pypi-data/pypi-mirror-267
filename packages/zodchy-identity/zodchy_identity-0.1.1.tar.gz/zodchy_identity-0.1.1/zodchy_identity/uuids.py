import abc
import typing
import uuid

T = typing.TypeVar("T")


class IdentifiersFactory(abc.ABC, typing.Generic[T]):
    def random(self) -> T: ...

    def derived(self, value: str | bytes) -> T: ...


class UUIDIdentifiersFactory:
    def __init__(
        self,
        namespace: uuid.UUID | None = None
    ):
        if not namespace:
            self._namespace = uuid.NAMESPACE_DNS
        else:
            self._namespace = namespace

    @staticmethod
    def random() -> uuid.UUID:
        return uuid.uuid4()

    def derived(self, value: str | bytes) -> uuid.UUID:
        return uuid.uuid5(self._namespace, value)
