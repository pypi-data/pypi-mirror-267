from collections import UserList
import typing as t


T = t.TypeVar('T')


NOTHING = object()


class XIndex(UserList):
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

    def shift(self, i: t.Union[slice, int]):
        if isinstance(i, slice):
            i = slice(
                None if i.start is None else self.shift_int(i.start),
                None if i.stop is None else self.shift_int(i.stop),
                i.step,
            )
        else:
            i = self.shift_int(i)
        return i

    def __getitem__(self, i):
        i = self.shift(i)
        return super().__getitem__(i)

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
