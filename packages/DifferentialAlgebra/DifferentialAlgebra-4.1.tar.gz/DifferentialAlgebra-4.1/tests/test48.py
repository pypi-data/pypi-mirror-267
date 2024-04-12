# positive_integer_roots

from sympy import *
from DifferentialAlgebra import *
import unittest

class TestDifferentialAlgebra(unittest.TestCase):
    def test_48(self):
        x,q,a,b = var('x,q,a,b')
        y1,y2 = indexedbase ('y1,y2')
        R = DifferentialRing (derivations = [x], blocks = [[y2,y1],[q,a,b]], parameters = [q,a,b], notation = 'jet')
        P = y1*y2*(q - 27)*(q-1)*(q**2 - 2) + y1**2*(q - 27)*(q-1)**2 + (q - 27)*(q-1)*(q - 3)
        L = R.positive_integer_roots (P, q)
        self.assertEqual (L, [1, 27])

if __name__ == '__main__':
    unittest.main()
