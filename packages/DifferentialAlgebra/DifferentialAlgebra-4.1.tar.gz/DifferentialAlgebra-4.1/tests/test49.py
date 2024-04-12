# DL_prolongation_prerequisites

from sympy import *
from DifferentialAlgebra import *
import unittest

class TestDifferentialAlgebra(unittest.TestCase):
    def test_49(self):
        x,q = var('x,q')
        y = indexedbase ('y')
        params = [y[i] for i in range (9, -1, -1)]
        R = DifferentialRing (derivations = [x], blocks = [y,q,params], parameters = params, notation = 'jet')
        A = RegularDifferentialChain ([y[1]], R) 
        P = y*y[x,x] + y[x]**2 - 6*y
        ybar = Add (*[y[i]*x**i/factorial(i) for i in range (1,10)])
        point = { y:ybar, x:0 }
        L = A.prolongation_prerequisites (q, point, edo=P)
        self.assertEqual (L, [ y[x,x], 2, 2, 2, y[2]/Integer(2), 1/Integer(2)*(y[2]*q**2 + 15*y[2]*q + 56*y[2] - 12) ])

if __name__ == '__main__':
    unittest.main()
