import unittest

import permutation

class PermutationTest(unittest.TestCase):

  def test_identity(self):
    iden = permutation.Permutation([0,1,2])
    self.assertEqual(iden, permutation.Permutation.identity(3))

  def test_mul(self):
    p1 = permutation.Permutation([0,2,1])
    p2 = permutation.Permutation([2,0,1])
    self.assertEqual(p2*p1, permutation.Permutation([1,0,2]))

if __name__ == '__main__':
  unittest.main()
