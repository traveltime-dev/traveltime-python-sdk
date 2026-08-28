from traveltimepy.itertools import flatten, sliding, split


def test_sliding_splits_into_windows():
    assert sliding([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]
    assert sliding([], 2) == []


def test_split_pads_the_shorter_side_with_empty_lists():
    assert split([1, 2, 3], ["a"], 2) == [([1, 2], ["a"]), ([3], [])]
    assert split([], ["a", "b", "c"], 2) == [([], ["a", "b"]), ([], ["c"])]
    assert split([], [], 2) == []


def test_flatten():
    assert flatten([[1, 2], [], [3]]) == [1, 2, 3]
