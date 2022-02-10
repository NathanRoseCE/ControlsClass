from .one_a import *
from sympy import Matrix, simplify, exp, symbols, integrate

def get_integrand(A: Matrix, B: Matrix):
    stm = STM_laplace_inverse(A) # from problem 1
    t, tau = symbols('t, ' + r'\tau')
    u = exp(2*t)
    return simplify((stm.subs(t, t-tau) * B.subs(t, tau) * u.subs(t, tau)))
    
def zero_state(A: Matrix, B: Matrix):
    integrand = get_integrand(A,B)
    t, tau = symbols('t, ' + r'\tau')
    return simplify(integrate(integrand, (tau, 0, t)))
