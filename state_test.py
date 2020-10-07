import copy
import unittest

import state


class StateTest(unittest.TestCase):

  def test_validate(self):
    cube = state.State.solved()
    cube.validate()
    for plane in range(6):
      for _ in range(4):
        cube.rotate(plane)
        cube.validate()

  def test_four_rotations_do_nothing(self):
    solved = state.State.solved()
    for plane in range(6):
      cube = state.State.solved()
      for i in range(4):
        cube.rotate(plane)
        if i == 3:
          self.assertEqual(cube, solved)
        else:
          self.assertNotEqual(cube, solved)

  def test_hamming(self):
    solved = state.State.solved()
    for plane in range(6):
      rotated = state.State.solved()
      rotated.rotate(0)
      self.assertEqual(rotated.hamming_dist(solved), 12)
      self.assertEqual(rotated.naive_cost(), 12)

  def test_zero_cost(self):
    solved = state.State.solved()
    self.assertEqual(0, solved.naive_cost())
    self.assertEqual(0, solved.cube_cost())

  def test_cost(self):
    s = state.State(
        front='OORYWRRGY',
        back='WBRRYWWOW',
        up='YOOGRYYWB',
        down='WOOWOGBYR',
        left='GWGRBBOBB',
        right='YRGBGGBYG')
    self.assertEqual(40, s.naive_cost())
    self.assertEqual(40, s.cube_cost())

  def test_rotate_back(self):
    start = state.State(
        front='OORYWRRGY',
        back='WBRRYWWOW',
        up='YOOGRYYWB',
        down='WOOWOGBYR',
        left='GWGRBBOBB',
        right='YRGBGGBYG')
    rotated = copy.deepcopy(start)
    rotated.rotate(state.ROTATIONS.index('B'))
    self.assertEqual(
      rotated,
      state.State(
          front='OORYWRRGY',
          back='WRWOYBWWR',
          up='GGGGRYYWB',
          down='WOOWOGGRO',
          left='OWGOBBYBB',
          right='YRRBGYBYB'))

  def test_rotate_down(self):
    start = state.State(
        front='OORYWRRGY',
        back='WRWOYBWWR',
        up='GGGGRYYWB',
        down='WOOWOGGRO',
        left='OWGOBBYBB',
        right='YRRBGYBYB')
    rotated = copy.deepcopy(start)
    rotated.rotate(state.ROTATIONS.index('D'))
    self.assertEqual(
        rotated,
        state.State(
            front='OORYWRYBB',
            back='WRWOYBBYB',
            up='GGGGRYYWB',
            down='GWWROOOGO',
            left='OWGOBBWWR',
            right='YRRBGYRGY'))

  def test_encode_decode(self):
    start = state.State(
        front='OORYWRRGY',
        back='WRWOYBWWR',
        up='GGGGRYYWB',
        down='WOOWOGGRO',
        left='OWGOBBYBB',
        right='YRRBGYBYB')
    self.assertEqual(start, state.State.decode(start.encode()))

  def test_permutations(self):
    lst = 'abc'
    perm = state._permutations(lst)
    perm = set([''.join(e) for e in perm])
    self.assertSetEqual(perm, {'acb', 'bac', 'bca', 'cba', 'cab'})


if __name__ == '__main__':
  unittest.main()
