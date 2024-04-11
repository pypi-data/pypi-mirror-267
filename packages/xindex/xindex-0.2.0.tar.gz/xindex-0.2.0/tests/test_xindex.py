import pytest

from xindex import XIndex


@pytest.fixture
def xlist():
    return XIndex([2, 3, 4, 5])


@pytest.fixture
def xindex():
    return XIndex([2, 3, 4, 5], i=2)


def test_lt(
    xlist,
    xindex,
):
    assert xlist < [3, 3, 4, 5]
    assert xindex < [3, 3, 4, 5]


def test_le(
    xlist,
    xindex,
):
    assert xlist <= [2, 3, 4, 5]
    assert xindex <= [2, 3, 4, 5]


def test_eq(
    xlist,
    xindex,
):
    assert xlist == [2, 3, 4, 5]
    assert xindex == [2, 3, 4, 5]


def test_gt(
    xlist,
    xindex,
):
    assert xlist > [1, 3, 4, 5]
    assert xindex > [1, 3, 4, 5]


def test_ge(
    xlist,
    xindex,
):
    assert xlist >= [2, 3, 4, 5]
    assert xindex >= [2, 3, 4, 5]


@pytest.mark.parametrize(
    ('i'),
    [2, 3, 4, 5],
)
def test_contains(
    i: int,
    xlist,
    xindex,
):
    assert i in xlist
    assert i in xindex


def test_len(
    xlist,
    xindex,
):
    assert len(xlist) == 4
    assert len(xindex) == 4


def test_getitem_slice_all(
    xindex,
    xlist,
):
    assert xlist[:] == [2, 3, 4, 5]
    assert xlist[slice(None)] == [2, 3, 4, 5]

    assert xindex[:] == [2, 3, 4, 5]
    assert xindex[slice(None)] == [2, 3, 4, 5]


def test_getitem_slice_stop(
    xlist,
    xindex,
):
    assert xlist[:0] == []
    assert xlist[:1] == [2]
    assert xlist[:2] == [2, 3]
    assert xlist[slice(0)] == []
    assert xlist[slice(1)] == [2]
    assert xlist[slice(2)] == [2, 3]

    assert xindex[:2] == []
    assert xindex[:3] == [2]
    assert xindex[:4] == [2, 3]
    assert xindex[slice(2)] == []
    assert xindex[slice(3)] == [2]
    assert xindex[slice(4)] == [2, 3]


def test_getitem_slice_negativestop(
    xlist,
    xindex,
):
    assert xlist[:-1] == [2, 3, 4]
    assert xlist[:-2] == [2, 3]
    assert xlist[:-3] == [2]
    assert xlist[:-4] == []
    assert xlist[slice(-1)] == [2, 3, 4]
    assert xlist[slice(-2)] == [2, 3]
    assert xlist[slice(-3)] == [2]
    assert xlist[slice(-4)] == []

    assert xindex[:-1] == [2, 3, 4]
    assert xindex[:-2] == [2, 3]
    assert xindex[:-3] == [2]
    assert xindex[:-4] == []
    assert xindex[slice(-1)] == [2, 3, 4]
    assert xindex[slice(-2)] == [2, 3]
    assert xindex[slice(-3)] == [2]
    assert xindex[slice(-4)] == []


def test_getitem_slice_start_stop(
    xindex,
    xlist,
):
    assert xlist[1:3] == [3, 4]
    assert xlist[slice(1, 3)] == [3, 4]

    assert xindex[3:5] == [3, 4]
    assert xindex[slice(3, 5)] == [3, 4]


def test_getitem_slice_start_stop_step(
    xindex,
    xlist,
):
    assert xlist[0::1] == [2, 3, 4, 5]
    assert xlist[0::2] == [2, 4]
    assert xlist[slice(0, None, 1)] == [2, 3, 4, 5]
    assert xlist[slice(0, None, 2)] == [2, 4]

    assert xindex[2::1] == [2, 3, 4, 5]
    assert xindex[2::2] == [2, 4]
    assert xindex[slice(2, None, 1)] == [2, 3, 4, 5]
    assert xindex[slice(2, None, 2)] == [2, 4]


def test_getitem_slice_start(
    xindex,
    xlist,
):
    assert xlist[0:] == [2, 3, 4, 5]
    assert xlist[1:] == [3, 4, 5]
    assert xlist[slice(0, None)] == [2, 3, 4, 5]
    assert xlist[slice(1, None)] == [3, 4, 5]

    assert xindex[2:] == [2, 3, 4, 5]
    assert xindex[3:] == [3, 4, 5]
    assert xindex[slice(2, None)] == [2, 3, 4, 5]
    assert xindex[slice(3, None)] == [3, 4, 5]


@pytest.mark.parametrize(
    ('i'),
    [2, 3, 4, 5],
)
def test_getitem(
    i: int,
    xlist,
    xindex,
):
    assert xlist[i - 2] == i
    assert xindex[i] == i


@pytest.mark.parametrize(
    ('i'),
    [6, 7],
)
def test_getitem_out_of_range_big(
    i: int,
    xlist,
    xindex,
):
    with pytest.raises(IndexError) as excinfo:
        xlist[i - 2]

    with pytest.raises(IndexError) as excinfo:
        xindex[i]
    assert 'list index out of range' == str(excinfo.value)


@pytest.mark.parametrize(
    ('i'),
    [0, 1],
)
def test_getitem_out_of_range_small(
    i: int,
    xindex,
):
    with pytest.raises(IndexError) as excinfo:
        xindex[i]
    assert f'list index {i} out of range' == str(excinfo.value)


@pytest.mark.parametrize(
    ('i', 'expected'),
    [
        (-1, 5),
        (-2, 4),
        (-3, 3),
        (-4, 2),
    ],
)
def test_getitem_negative_indices(
    i: int,
    expected: int,
    xlist,
    xindex,
):
    assert xlist[i] == expected
    assert xindex[i] == expected


@pytest.mark.parametrize(
    ('i'),
    [-5, -6],
)
def test_getitem_negative_indices_out_of_range(
    i: int,
    xlist,
    xindex,
):
    with pytest.raises(IndexError) as excinfo:
        xlist[i]
    assert 'list index out of range' == str(excinfo.value)

    with pytest.raises(IndexError) as excinfo:
        xindex[i]
    assert 'list index out of range' == str(excinfo.value)


def test_setitem(
    xlist,
    xindex,
):
    xlist[0] = None
    assert xlist == [None, 3, 4, 5]

    xindex[2] = None
    assert xindex == [None, 3, 4, 5]


def test_delitem(
    xlist,
    xindex,
):
    del xlist[0]
    assert xlist == [3, 4, 5]

    del xindex[2]
    assert xindex == [3, 4, 5]


def test_insert(
    xlist,
    xindex,
):
    xlist.insert(2, None)
    assert xlist == [2, 3, None, 4, 5]

    xindex.insert(4, None)
    assert xindex == [2, 3, None, 4, 5]


def test_pop(
    xlist,
    xindex,
):
    xlist.pop()
    assert xlist == [2, 3, 4]
    xlist.pop(1)
    assert xlist == [2, 4]

    xindex.pop()
    assert xindex == [2, 3, 4]
    xindex.pop(3)
    assert xindex == [2, 4]
