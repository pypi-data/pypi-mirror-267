# DL_prolongation_prerequisites

from sympy import *
from DifferentialAlgebra import *
import unittest

class TestDifferentialAlgebra(unittest.TestCase):
    def test_50(self):
        x,q = var('x,q')
        y = indexedbase ('y')
        params = [y[i] for i in range (9, -1, -1)]
        R = DifferentialRing (derivations = [x], blocks = [y,q,params], parameters = params, notation = 'jet')
        A = RegularDifferentialChain ([], R) 
        P = y[x,x]**2 + y[x] + y + 1
        ybar = y[0] + y[1]*x
        point = { y:ybar, x:0 }
        L = A.prolongation_prerequisites (q, point, edo=P)
        self.assertEqual (L, [y[x,x], 2, oo, oo, 0, 0])

if __name__ == '__main__':
    unittest.main()
