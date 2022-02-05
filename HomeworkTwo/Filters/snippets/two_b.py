from .one_a import *
from sympy import Matrix, simplify, exp, symbols, integrate


def zero_state(A: Matrix, B: Matrix):
    stm = STM_laplace_inverse(A)
    t, tau = symbols('t, ' + r'\tau')
    u = exp(2*t)
    integrand = simplify((stm * B * u)).subs(t, tau)
    return simplify(integrate(integrand, (tau, 0, t)))


