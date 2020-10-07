import unittest
from unittest import mock

import k_best


class KBestTest(unittest.TestCase):
  def test_merge(self):
    k1 = k_best.KBest(3)
    k1.maybe_add('k1a', mock.Mock(), 3)
    k1.maybe_add('k1b', mock.Mock(), 5)
    k1.maybe_add('k1c', mock.Mock(), 7)
    k2 = k_best.KBest(3)
    k2.maybe_add('k2a', mock.Mock(), 2)
    k2.maybe_add('k2b', mock.Mock(), 4)
    k2.maybe_add('k2c', mock.Mock(), 6)
    merged = k_best.merge_kbests([k1, k2], 3)
    self.assertSequenceEqual([item.path for item in merged.items],
                             ['k2a', 'k1a', 'k2b'])


if __name__ == '__main__':
  unittest.main()
