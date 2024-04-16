import collections.abc
import typing


class Pipe:
    def __init__(self, stream: collections.abc.Iterable[collections.abc.MutableMapping]):
        self._stream = stream
        self._mappers = []
        self._filters = []

    def map(self, *func: collections.abc.Callable) -> typing.Self:
        self._mappers.extend(list(func))
        return self

    def filter(self, func: collections.abc.Callable) -> typing.Self:
        self._filters.append(func)
        return self

    def collect(self, func: collections.abc.Callable = None) -> typing.Any:
        stream = self._stream
        for filter_func in self._filters:
            stream = filter(filter_func, stream)

        for map_func in self._mappers:
            stream = map(map_func, stream)

        return func(stream) if func else stream
