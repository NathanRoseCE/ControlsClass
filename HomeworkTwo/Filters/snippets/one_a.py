import numpy as np
import sympy
from sympy import eye, shape, simplify, inverse_laplace_transform


def STM_laplace_inverse(A: np.matrix) -> None:
    s, t = sympy.symbols('s, t')
    s_I = eye(shape(A)[0])*s
    return simplify(
        inverse_laplace_transform((s_I - A).inv(), s, t)
    )
