import itertools
from typing import List, TypeVar, Tuple

T = TypeVar('T')
R = TypeVar('R')


def sliding(values: List[T], window_size: int) -> List[List[T]]:
    return [values[i:i+window_size] for i in range(0, len(values), window_size)]


def split(left: List[T], right: List[R], window_size: int) -> List[List[Tuple[T, R]]]:
    return list(itertools.zip_longest(sliding(left, window_size), sliding(right, window_size), fillvalue=[]))
