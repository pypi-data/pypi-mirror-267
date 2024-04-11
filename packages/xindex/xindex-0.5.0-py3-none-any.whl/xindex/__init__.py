from collections import UserList
import typing as t

from .typealiases import IndexOrSlice


T = t.TypeVar('T')


class XIndex(UserList[T]):
    data: list[T]

    def __init__(self, initlist: t.Optional[t.Iterable[T]] = None, i: int = 0):
        assert i >= 0
        super().__init__(initlist)
        self.i = i

    def shift_int(self, i: int):
        shift = self.i
        if 0 <= i < shift:
            raise IndexError(f'list index {i} out of range')
        if shift <= i:
            i -= shift
        return i

    # @t.overload
    # def shift(self, i: t.SupportsIndex) -> int: ...
    # @t.overload
    # def shift(self, i: slice) -> slice: ...
    def shift(self, i: IndexOrSlice):
        if isinstance(i, slice):
            i = slice(
                None if i.start is None else self.shift_int(i.start),
                None if i.stop is None else self.shift_int(i.stop),
                i.step,
            )
        else:
            i = self.shift_int(t.cast(int, i))
        return i

    @t.overload
    def __getitem__(self, i: t.SupportsIndex, /) -> T: ...
    @t.overload
    def __getitem__(self, i: slice, /) -> 'XIndex[T]': ...
    def __getitem__(self, i: IndexOrSlice):
        i = self.shift(i)
        if isinstance(i, slice):
            return XIndex(self.data[i], self.i)
        return self.data[i]

    def __setitem__(self, i, item):
        i = self.shift(i)
        return super().__setitem__(i, item)

    def __delitem__(self, i):
        i = self.shift(i)
        return super().__delitem__(i)

    def insert(self, i, item):
        i = self.shift_int(i)
        return super().insert(i, item)

    def pop(self, i=-1):
        i = self.shift_int(i)
        return super().pop(i)

    def enumerate(self):
        return enumerate(iterable=self.data, start=self.i)


if 0:
    xi = XIndex([1])
    ssss = xi[slice(0, 2)]
    eeee = xi[0]

    llll = list(xi)
