from .one_a import *
from sympy import Matrix, simplify


def zero_input_equation(A: Matrix, x_0: Matrix):
    stm = STM_laplace_inverse(A) #from problem 1 
    return simplify(stm * x_0)


