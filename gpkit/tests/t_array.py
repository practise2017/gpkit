import unittest
from gpkit import Monomial, Posynomial
from gpkit.utils import monify, vectify
from gpkit.array import array


class t_array(unittest.TestCase):

    def test_array_mult(self):
        x = vectify('x', 3)
        x0, x1, x2 = monify('x0 x1 x2')
        p = x0**2 + x1**2 + x2**2
        self.assertEqual(x.dot(x), p)
        m = array([[x0**2, x0*x1, x0*x2],
                   [x0*x1, x1**2, x1*x2],
                   [x0*x2, x1*x2, x2**2]])
        self.assertEqual(x.outer(x), m)

    def test_elementwise_mult(self):
        x = vectify('x', 3)
        x0, x1, x2 = monify('x0 x1 x2')
        # multiplication
        v = array([1, 2, 3]).T
        p = array([1*x0, 2*x1, 3*x2]).T
        self.assertEqual(x*v, p)
        # division
        p2 = array([x0, x1/2, x2/3]).T
        self.assertEqual(x/v, p2)
        # power
        p3 = array([x0**2, x1**2, x2**2]).T
        self.assertEqual(x**2, p3)

    def test_constraint_gen(self):
        x = vectify('x', 3)
        x0, x1, x2 = monify('x0 x1 x2')
        v = array([1, 2, 3]).T
        p = [x0, x1/2, x2/3]
        self.assertEqual(x <= v, p)
        self.assertEqual(x < v, p)

    def test_substition(self):
        x = vectify('x', 3)
        c = {'x': [1, 2, 3]}
        s = array([Monomial({}, e) for e in [1, 2, 3]])
        self.assertEqual(x.sub(c), s)
        p = x**2
        s2 = array([Monomial({}, e) for e in [1, 4, 9]])
        self.assertEqual(p.sub(c), s2)
        d = p.sum()
        self.assertEqual(d.sub(c), array(Monomial({}, 14)))


tests = [t_array]

if __name__ == '__main__':
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()

    for t in tests:
        suite.addTests(loader.loadTestsFromTestCase(t))

    unittest.TextTestRunner(verbosity=2).run(suite)