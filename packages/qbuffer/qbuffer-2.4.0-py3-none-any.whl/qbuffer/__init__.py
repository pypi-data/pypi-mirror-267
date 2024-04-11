from collections import deque
import typing as t


T = t.TypeVar('T')


class Qbuffer(t.Generic[T]):
    def __init__(
        self,
        *,
        maxlen: int,
        callback: t.Callable[[T], t.Any],
        flush_callback: t.Callable[[], t.Any] = lambda: None,
    ):
        self.maxlen = maxlen
        self.callback = callback
        self.flush_callback = flush_callback
        self.data: deque[T] = deque()

    def append(self, item: T, *, flush=False):
        self.data.append(item)
        if len(self.data) >= self.maxlen:
            self.flush()
        if flush:
            self.flush()

    def extend(self, items: t.Iterable[T], *, flush=False):
        for item in items:
            self.append(item)
        if flush:
            self.flush()

    def flush(self):
        while self.data:
            self.callback(self.data.popleft())
        self.flush_callback()

    ###

    def close(self):
        self.flush()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def __del__(self):
        self.close()
