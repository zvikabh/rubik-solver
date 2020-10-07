import dataclasses
import frozendict
import itertools
from typing import Any, List, Sequence, Tuple, Union

COLORS = ('W', 'R', 'G', 'B', 'Y', 'O')
COLORS_TO_INDICES = frozendict.frozendict(
  {'W': 0, 'R': 1, 'G': 2, 'B': 3, 'Y': 4, 'O': 5})
ROTATIONS = ('U', 'D', 'L', 'R', 'F', 'B')


def hamming_dist(s1: Sequence[Any], s2: Sequence[Any]) -> int:
  return ((s1[0] != s2[0]) +
          (s1[1] != s2[1]) +
          (s1[2] != s2[2]) +
          (s1[3] != s2[3]) +
          (s1[4] != s2[4]) +
          (s1[5] != s2[5]) +
          (s1[6] != s2[6]) +
          (s1[7] != s2[7]) +
          (s1[8] != s2[8]))


def rotate_clockwise(face: Sequence[int]) -> List[int]:
  return [face[6], face[3], face[0], face[7], face[4], face[1], face[8],
          face[5], face[2]]


def _init_face(values: Union[str, Sequence[int]]) -> List[int]:
  if isinstance(values, str):
    return [COLORS_TO_INDICES[e] for e in values]
  return list(values)


def _permutations(lst: Sequence[Any]):
  return list(itertools.permutations(lst))[1:]


FUL_CORRECT_CORNER = (0, 1, 3)
FUR_CORRECT_CORNER = (0, 1, 2)
FDL_CORRECT_CORNER = (0, 5, 3)
FDR_CORRECT_CORNER = (0, 5, 2)
ULB_CORRECT_CORNER = (1, 3, 4)
URB_CORRECT_CORNER = (1, 2, 4)
BRD_CORRECT_CORNER = (4, 2, 5)
BLD_CORRECT_CORNER = (4, 3, 5)
CORRECT_CORNER_VALS = (
  FUL_CORRECT_CORNER, FUR_CORRECT_CORNER, FDL_CORRECT_CORNER,
  FDR_CORRECT_CORNER, ULB_CORRECT_CORNER, URB_CORRECT_CORNER,
  BRD_CORRECT_CORNER, BLD_CORRECT_CORNER)
HALF_CORRECT_CORNER_VALS = tuple(
  _permutations(val) for val in CORRECT_CORNER_VALS)


@dataclasses.dataclass
class State:
  """State of the Rubik's cube.

  Each attribute is a 9-element list describing the 9 colors in a given face.
  The elements are ordered lexicographically when looking directly at the face.
  Each element is one of range(6) representing 'W', 'R', 'G', 'B', 'Y', 'O',
  respectively (see the COLORS list above).
  The central char in each face must be a constant value, as verified by
  State.validate().
  """
  front: List[int]
  back: List[int]
  up: List[int]
  down: List[int]
  left: List[int]
  right: List[int]

  def __init__(self, front: Union[str, Sequence[int]],
               back: Union[str, Sequence[int]], up: Union[str, Sequence[int]],
               down: Union[str, Sequence[int]], left: Union[str, Sequence[int]],
               right: Union[str, Sequence[int]]):
    self.front = _init_face(front)
    self.back = _init_face(back)
    self.up = _init_face(up)
    self.down = _init_face(down)
    self.left = _init_face(left)
    self.right = _init_face(right)
    self.validate()

  @staticmethod
  def solved() -> 'State':
    """A solved Rubik's cube."""
    return State(
      front='WWWWWWWWW',
      up='RRRRRRRRR',
      right='GGGGGGGGG',
      left='BBBBBBBBB',
      back='YYYYYYYYY',
      down='OOOOOOOOO')

  def encode(self) -> Tuple[int, ...]:
    """Encode to a hashtable type."""
    return tuple(
      self.front + self.back + self.up + self.down + self.left + self.right)

  @staticmethod
  def decode(encoded: Tuple[int, ...]) -> 'State':
    """Opposite of encode."""
    assert len(encoded) == 54
    return State(encoded[:9], encoded[9:18], encoded[18:27], encoded[27:36],
                 encoded[36:45], encoded[45:])

  def __str__(self) -> str:
    result = ''
    for face_name in ['front', 'back', 'up', 'down', 'left', 'right']:
      face = getattr(self, face_name)
      result += '%6s: ' % face_name
      result += '%s%s%s %s%s%s %s%s%s' % (tuple(COLORS[e] for e in face))
      result += ' (%d matches)' % sum(e == face[4] for e in face)
      result += '\n'
    return result

  def __repr__(self) -> str:
    face_reprs = []
    for face_name in ['front', 'back', 'up', 'down', 'left', 'right']:
      face = getattr(self, face_name)
      face_repr = '%s=\'%s\'' % (face_name, ''.join(COLORS[e] for e in face))
      face_reprs.append(face_repr)
    return 'State(' + ', '.join(face_reprs) + ')'

  def validate(self) -> None:
    assert self.front[4] == 0
    assert self.up[4] == 1
    assert self.right[4] == 2
    assert self.left[4] == 3
    assert self.back[4] == 4
    assert self.down[4] == 5
    for l in (self.front, self.back, self.up, self.down, self.left, self.right):
      assert len(l) == 9
      assert all(i in range(6) for i in l)
    merged = (
        self.front + self.up + self.right + self.left + self.back + self.down)
    for color in range(6):
      assert sum(i == color for i in merged) == 9

  def hamming_dist(self, other: 'State') -> int:
    """Hamming distance to another State."""
    return (hamming_dist(self.front, other.front) +
            hamming_dist(self.back, other.back) +
            hamming_dist(self.up, other.up) +
            hamming_dist(self.down, other.down) +
            hamming_dist(self.left, other.left) +
            hamming_dist(self.right, other.right))

  def naive_cost(self) -> int:
    """Number of squares with the wrong color."""
    return (hamming_dist(self.front, [0] * 9) +
            hamming_dist(self.up, [1] * 9) +
            hamming_dist(self.right, [2] * 9) +
            hamming_dist(self.left, [3] * 9) +
            hamming_dist(self.back, [4] * 9) +
            hamming_dist(self.down, [5] * 9))

  def cube_cost(self) -> int:
    """Number of cubes in the wrong location.
    Cubes in the correct location with the wrong orientation have a half cost.
    """
    n_correct = 0
    n_half = 0
    
    # Corners
    ful = (self.front[0], self.up[6], self.left[2])
    fur = (self.front[2], self.up[8], self.right[0])
    fdl = (self.front[6], self.down[0], self.left[8])
    fdr = (self.front[8], self.down[2], self.right[6])
    ulb = (self.up[0], self.left[0], self.back[2])
    urb = (self.up[2], self.right[2], self.back[0])
    brd = (self.back[6], self.right[8], self.down[8])
    bld = (self.back[8], self.left[6], self.down[6])
    actuals = (ful, fur, fdl, fdr, ulb, urb, brd, bld)
    for actual, correct, half in zip(actuals, CORRECT_CORNER_VALS,
                                     HALF_CORRECT_CORNER_VALS):
      if actual == correct:
        n_correct += 1
      elif actual in half:
        n_half += 1

    # Edges
    n_correct += (self.front[1] == 0 and self.up[7] == 1)
    n_correct += (self.front[3] == 0 and self.left[5] == 3)
    n_correct += (self.front[5] == 0 and self.right[3] == 2)
    n_correct += (self.front[7] == 0 and self.down[1] == 5)
    n_correct += (self.up[3] == 1 and self.left[1] == 3)
    n_correct += (self.up[5] == 1 and self.right[1] == 2)
    n_correct += (self.down[3] == 5 and self.left[7] == 3)
    n_correct += (self.down[5] == 5 and self.right[7] == 2)
    n_correct += (self.back[1] == 4 and self.up[1] == 1)
    n_correct += (self.back[5] == 4 and self.left[3] == 3)
    n_correct += (self.back[3] == 4 and self.right[5] == 2)
    n_correct += (self.back[7] == 4 and self.down[7] == 5)
    
    return 40 - 2 * n_correct - n_half

  def rotate(self, plane: int) -> None:
    """Rotates a given plane, clockwise when looking at the plane.

    Args:
      plane: Which plane to rotate. Values are given by the ROTATIONS const.
    """
    if plane == 0:  # up
      self.up = rotate_clockwise(self.up)
      tmp = self.front[:3]
      self.front[:3] = self.right[:3]
      self.right[:3] = self.back[:3]
      self.back[:3] = self.left[:3]
      self.left[:3] = tmp
    elif plane == 1:  # down
      self.down = rotate_clockwise(self.down)
      tmp = self.front[6:]
      self.front[6:] = self.left[6:]
      self.left[6:] = self.back[6:]
      self.back[6:] = self.right[6:]
      self.right[6:] = tmp
    elif plane == 2:  # left
      self.left = rotate_clockwise(self.left)
      for f, u, b, d in [(0, 0, 8, 0), (3, 3, 5, 3), (6, 6, 2, 6)]:
        tmp = self.front[f]
        self.front[f] = self.up[u]
        self.up[u] = self.back[b]
        self.back[b] = self.down[d]
        self.down[d] = tmp
    elif plane == 3:  # right
      self.right = rotate_clockwise(self.right)
      for f, d, b, u in [(2, 2, 6, 2), (5, 5, 3, 5), (8, 8, 0, 8)]:
        tmp = self.front[f]
        self.front[f] = self.down[d]
        self.down[d] = self.back[b]
        self.back[b] = self.up[u]
        self.up[u] = tmp
    elif plane == 4:  # front
      self.front = rotate_clockwise(self.front)
      for u, l, d, r in [(6, 8, 2, 0), (7, 5, 1, 3), (8, 2, 0, 6)]:
        tmp = self.up[u]
        self.up[u] = self.left[l]
        self.left[l] = self.down[d]
        self.down[d] = self.right[r]
        self.right[r] = tmp
    elif plane == 5:  # back
      self.back = rotate_clockwise(self.back)
      for u, r, d, l in [(0, 2, 8, 6), (1, 5, 7, 3), (2, 8, 6, 0)]:
        tmp = self.up[u]
        self.up[u] = self.right[r]
        self.right[r] = self.down[d]
        self.down[d] = self.left[l]
        self.left[l] = tmp
    else:
      raise ValueError(f'Invalid plane {plane}')
