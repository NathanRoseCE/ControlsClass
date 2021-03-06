import numpy as np
import sympy
from sympy import eye, shape, simplify, inverse_laplace_transform, Matrix

def sI_A(A: Matrix):
    s = sympy.symbols('s')
    s_I = eye(shape(A)[0])*s
    return simplify(s_I-A)

def STM_laplace_inverse(A: Matrix):
    s, t = sympy.symbols('s, t')
    return simplify(
        inverse_laplace_transform((sI_A(A)).inv(), s, t)
    )
