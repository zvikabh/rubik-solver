from dataclasses import dataclass
from typing import List, Optional, Sequence

from state import State


@dataclass
class Item:
  path: Optional[List[int]] = None
  state: Optional[State] = None
  encoded_state: Optional[int] = None
  cost: int = 1000


class KBest:

  def __init__(self, k: int):
    self.items = [Item() for _ in range(k)]

  def maybe_add(self, path: List[int], state: State, cost: int):
    if state is None:
      return
    if self.items[-1].cost < cost:
      return  # Cost too high
    encoded_state = state.encode()
    if any(encoded_state == item.encoded_state for item in self.items):
      return  # Item already exists
    self.items[-1].path = path
    self.items[-1].state = state
    self.items[-1].encoded_state = encoded_state
    self.items[-1].cost = cost
    self.items.sort(key=lambda item: item.cost)

  @property
  def best_cost(self):
    return self.items[0].cost

  @property
  def worst_cost(self):
    return self.items[-1].cost

  @property
  def k(self):
    return len(self.items)


def merge_kbests(seq: Sequence[KBest], k: int) -> KBest:
  """Merge a sequence of KBest objects.

  We take elements from the different input objects in an attempt to increase
  diversity. For example, if all items in all inputs have the same costs, the
  output will contain items from all inputs.
  """
  res = KBest(k)
  max_k = max(kbest.k for kbest in seq)
  for i in range(max_k):
    for kbest in seq:
      if i < kbest.k:
        res.maybe_add(kbest.items[i].path, kbest.items[i].state,
                      kbest.items[i].cost)
  return res
