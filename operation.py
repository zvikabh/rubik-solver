from typing import Mapping, Union

import frozendict

import permutation as perm

_CORNER_NAMES = frozendict.frozendict({
  'BUL': 0, 'BUR': 1, 'FUL': 2, 'FUR': 3, 'BDL': 4, 'BDR': 5, 'FDL': 6,
  'FDR': 7})
_EDGE_NAMES = frozendict.frozendict({
  'BU': 0, 'RU': 1, 'FU': 2, 'LU': 3, 'BL': 4, 'BR': 5, 'FL': 6, 'FR': 7,
  'BD': 8, 'RD': 9, 'FD': 10, 'LD': 11})

def _translate_from_names(src: Mapping[str, str],
                          names: Mapping[str, int]) -> perm.Permutation:
  num_dict = {names[k]: names[v] for k, v in src.items()}
  p = [num_dict.get(i, i) for i in range(len(names))]
  return perm.Permutation(p)


class RubikOperation:
  """Operation on a Rubik cube.

  The operation is represented as a permutation on the corner pieces and a
  permutation on the edge pieces.

  The description below assumes the cube is situated such that the centers are
  arranged as follows:
  * White - front
  * Yellow - back
  * Red - up
  * Orange - down
  * Blue - left
  * Green - right

  Attributes:
    corners: 8-Permutation object describing the permutation which would bring
      the corner pieces to their correct locations. The corner locations are
      arranged as defined by _CORNER_NAMES. For example, the first entry is the
      back up left (BUL) corner.
    edges: 12-Permutation object describing the permutation which would bring
      the edge pieces to their correct locations. These are arranged as defined
      by _EDGE_NAMES. For example, the first entry is the Up Back (UB) corner.
    TODO: Add permutations within a single block.
  """

  def __init__(self, corners: Union[perm.Permutation, Mapping[str, str]],
               edges: Union[perm.Permutation, Mapping[str, str]]):
    if isinstance(corners, dict):
      self.corners = _translate_from_names(corners, _CORNER_NAMES)
    else:
      self.corners = corners
    if isinstance(edges, dict):
      self.edges = _translate_from_names(edges, _EDGE_NAMES)
    else:
      self.edges = edges

  @classmethod
  def identity(cls):
    return cls(perm.Permutation.identity(8), perm.Permutation.identity(12))

  def __eq__(self, other: 'RubikOperation') -> bool:
    return self.corners == other.corners and self.edges == other.edges

  def __mul__(self, other: 'RubikOperation') -> 'RubikOperation':
    return RubikOperation(self.corners * other.corners,
                          self.edges * other.edges)

  def __str__(self) -> str:
    return f'Corners: {self.corners} ; Edges: {self.edges}'
