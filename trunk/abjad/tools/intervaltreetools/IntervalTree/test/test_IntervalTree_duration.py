from abjad.tools.intervaltreetools import *
import py.test


def test_IntervalTree_duration_01():
    a = TimeInterval(-1, 2)
    b = TimeInterval(0, 1)
    c = TimeInterval(1, 3)

    tree = IntervalTree(a)
    assert tree.duration == 3

    tree = IntervalTree(b)
    assert tree.duration == 1

    tree = IntervalTree(c)
    assert tree.duration == 2

    tree = IntervalTree([a, b])
    assert tree.duration == 3

    tree = IntervalTree([a, c])
    assert tree.duration == 4

    tree = IntervalTree([b, c])
    assert tree.duration == 3

    tree = IntervalTree([a, b, c])
    assert tree.duration == 4
