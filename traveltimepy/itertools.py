import itertools
from typing import List, TypeVar, Tuple

T = TypeVar("T")
R = TypeVar("R")


def split(
    left: List[T], right: List[R], window_size: int
) -> List[Tuple[List[T], List[R]]]:
    def windows(values: List) -> List[List]:
        return [values[i : i + window_size] for i in range(0, len(values), window_size)]

    left_windows = windows(left)
    right_windows = windows(right)
    return [
        (
            left_windows[i] if i < len(left_windows) else [],
            right_windows[i] if i < len(right_windows) else [],
        )
        for i in range(max(len(left_windows), len(right_windows)))
    ]


def flatten(list_of_lists: List[List[T]]) -> List[T]:
    return list(itertools.chain.from_iterable(list_of_lists))
