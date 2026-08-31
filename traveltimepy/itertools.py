import itertools
from typing import List, TypeVar, Tuple, Optional

T = TypeVar("T")
R = TypeVar("R")


def sliding(values: List[T], window_size: int) -> List[List[T]]:
    return [values[i : i + window_size] for i in range(0, len(values), window_size)]


def split(
    left: List[T], right: List[R], window_size: int
) -> List[Tuple[List[T], List[R]]]:
    left_windows = sliding(left, window_size)
    right_windows = sliding(right, window_size)
    return [
        (
            left_windows[i] if i < len(left_windows) else [],
            right_windows[i] if i < len(right_windows) else [],
        )
        for i in range(max(len(left_windows), len(right_windows)))
    ]


def join_opt(values: Optional[List[str]], sep: str) -> Optional[str]:
    return sep.join(values) if values is not None and len(values) != 0 else None


def flatten(list_of_lists: List[List[T]]) -> List[T]:
    return list(itertools.chain.from_iterable(list_of_lists))
