import sympy
from sympy import cos, sin
from typing import Callable, Iterable, Tuple
from copy import deepcopy

def model_system(update: Callable[[sympy.Matrix, sympy.Matrix], sympy.Matrix],
                 output: Callable[[sympy.Matrix, sympy.Matrix], sympy.Matrix],
                 x_0: sympy.Matrix,
                 inputs: Iterable[sympy.Matrix],
                 *args,
                 **dargs) -> Iterable[Tuple]:
    """
    A generic model for any system can work with linear and nonlinear
    systems. update functions returns the next state, and output outputs
    the output matrix. Both of these functions take in state, system input,
    then *args.
    This function will return list of outputs

    This is an underlying function see other models for examples
    """
    outputs = []
    x = deepcopy(x_0)
    inputs = deepcopy(inputs)
    for r in inputs:
        x = update(x, r, *args, **dargs)
        outputs.append(output(x, r, *args, **dargs))
    return outputs

def non_linear_update(x: sympy.Matrix,
                      r: sympy.Matrix,
                      k: sympy.Matrix,
                      dt: float,
                      *args, **dargs) -> sympy.Matrix:
    """
    Non linear update equation to handle question 4
    @arg x is the previous state sys
    @arg r input before any feedback
    @arg k feedback matrix
    @returns next state
    """
    x_1 = float(x[0, 0])
    x_2 = float(x[1, 0])
    u = float( ((k*x) * r)[0,0] )
    dot_x_1 = -2*x_1 + x_2 + sin(x_2)
    dot_x_2 = -x_2*cos(x_1) + cos(2*x_1)*u
    new_x = sympy.Matrix([
        [x_1 + (dt*dot_x_1)],
        [x_2 + (dt*dot_x_2)]
    ])
    return new_x
    
def linear_update(x: sympy.Matrix,
                  r: sympy.Matrix,
                  A: sympy.Matrix,
                  B: sympy.Matrix,
                  dt: float,
                  k: sympy.Matrix=None,
                  *args, **dargs) -> sympy.Matrix:
    """
    Linear output equation
    """
    if k is not None:
        u = (k*x) * r
    else:
        u = r
    dx = A*x + B*r
    return x + (dx*dt)
def linear_output(x: sympy.Matrix,
                  r: sympy.Matrix,
                  C: sympy.Matrix,
                  D: sympy.Matrix,
                  *args, **dargs) -> sympy.Matrix:
    """
    Linear output equation
    """
    return C*x + D*r
