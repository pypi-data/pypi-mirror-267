# DL_prolongation_prerequisites / normal_form = True

from sympy import *
from DifferentialAlgebra import *
import unittest

class TestDifferentialAlgebra(unittest.TestCase):
    def test_51(self):
        x = var('x')
        q,D = var ('q,D')
        y = indexedbase ('y')
        params = [q, D] + [y[i] for i in range (6, -1, -1)]
        R = DifferentialRing (derivations = [x], blocks = [y, params], parameters = params, notation = 'jet')
        edo = y*y[x]**2 + y - D
        Dbar = 1
        ybar = y[0] + y[1]*x + y[2]*x**2/2
        point = { D:Dbar, y:ybar, x:0 }
        C = RegularDifferentialChain([edo, y[0]**3 - 1], R)
        L = C.prolongation_prerequisites (q, point, edo=edo)
        self.assertEqual (L, [y[x], 1, 0, 0, 2*y[0]*y[1], 2*y[0]*y[1]])
        C = RegularDifferentialChain([edo, y[0]-1, y[1], y[2]+1], R)
        L = C.prolongation_prerequisites (q, point, edo=edo)
        self.assertEqual (L, [y[x], 1, 1, 1, 2*y[0]*y[2] + 2*y[1]**2, 2*q*y[0]*y[2] + 2*q*y[1]**2 + 8*y[0]*y[2] + 9*y[1]**2 + 1])
        L = C.prolongation_prerequisites (q, point, edo=edo, normal_form=True)
        self.assertEqual (L, [y[x], 1, 1, 1, -2, -2*q - 7])

if __name__ == '__main__':
    unittest.main()
