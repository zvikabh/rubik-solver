import numpy as np
from typing import Sequence


class Permutation:

  def __init__(self, perm: Sequence[int]):
    assert set(perm) == set(range(len(perm)))
    self.perm = np.asarray(perm)

  @classmethod
  def identity(cls, length: int):
    return cls(range(length))

  def apply(self, source: Sequence[int]):
    assert len(source) == len(self.perm)
    return np.asarray(source)[self.perm]

  def __mul__(self, other: 'Permutation') -> 'Permutation':
    return Permutation(self.apply(other.perm))

  def __eq__(self, other: 'Permutation') -> bool:
    return np.all(self.perm == other.perm)

  def __str__(self) -> str:
    return str(self.perm)
