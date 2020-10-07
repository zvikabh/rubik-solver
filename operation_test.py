import unittest

import operation as op
import permutation as perm

class OperationTest(unittest.TestCase):

  def test_construct_from_names(self):
    expected_op = op.RubikOperation(
      corners=perm.Permutation([0, 1, 3, 7, 4, 5, 2, 6]),
      edges=perm.Permutation([0, 1, 7, 3, 4, 5, 2, 10, 8, 9, 6, 11]))
    actual_op = op.RubikOperation(
      corners={'FUL': 'FUR', 'FUR': 'FDR', 'FDR': 'FDL', 'FDL': 'FUL'},
      edges={'FU': 'FR', 'FR': 'FD', 'FD': 'FL', 'FL': 'FU'})
    self.assertEqual(expected_op, actual_op)


if __name__ == '__main__':
  unittest.main()
