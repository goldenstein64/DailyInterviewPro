from __future__ import annotations

from collections.abc import Sequence
from typing import overload


class ListView[T](Sequence[T]):
    def __init__(self, data: Sequence[T], view: Sequence[int] | None = None):
        self.data: Sequence[T] = data
        self.view: Sequence[int] = range(len(data)) if view is None else view

    @overload
    def __getitem__(self, index: int) -> T: ...
    @overload
    def __getitem__(self, index: slice) -> ListView[T]: ...
    def __getitem__(self, index: int | slice) -> T | ListView[T]:
        if type(index) is slice:
            return ListView(self.data, self.view[index])
        else:
            return self.data[self.view[index]]

    def __len__(self) -> int:
        return len(self.view)
