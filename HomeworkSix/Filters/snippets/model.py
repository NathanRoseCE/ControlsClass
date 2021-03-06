import sympy
from functools import cache
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

def observer_update_wrapper(x: sympy.Matrix,
                            r: sympy.Matrix,
                            system_update: Callable[[sympy.Matrix, sympy.Matrix], sympy.Matrix],
                            observer_update: Callable[[sympy.Matrix, sympy.Matrix], sympy.Matrix],
                            system_output: Callable[[sympy.Matrix, sympy.Matrix], sympy.Matrix],
                            k: sympy.Matrix=None,
                            *args, **dargs) -> Tuple[sympy.Matrix, sympy.Matrix]:
    system_x, est_x = x
    new_system_x = system_update(system_x, r, k=k, *args, **dargs)
    sys_y = system_output(new_system_x, r, *args, **dargs)
    new_est_x = observer_update(est_x, r, sys_y, k=k, *args, **dargs)
    if k is not None:
        u = (r - k*new_est_x)
        new_system_x = system_update(system_x, u, *args, **dargs)
    return new_system_x, new_est_x

def observer_update(x_est: sympy.Matrix,
                    r: sympy.Matrix,
                    y_sys: sympy.Matrix,
                    L: sympy.Matrix,
                    dt: float,
                    **dargs) -> None:
    # dargs["A"] = dargs["A"] - L*dargs["C"]
    # print(dargs["A"].eigenvals())
    new_est_x = linear_update(x_est, r, dt=dt, **dargs)
    y_est = linear_output(x_est, r, dt=dt, **dargs)
    new_est_x += L*(y_sys - y_est)*dt
    return new_est_x
                    
def observer_output_wrapper(x: sympy.Matrix,
                            r: sympy.Matrix,
                            *args, **dargs) -> Tuple[sympy.Matrix, sympy.Matrix]:
    """
    assuming the desired output is not the output itself but a condensed veriosn of the outptu
    """
    system_x, est_x = x
    condenser = sympy.Matrix([
        [1,1,1]
    ])
    system_out = (condenser * system_x)[0,0]
    observer_out = (condenser * est_x)[0,0]
    return [(condenser * system_x), (condenser * est_x)]


def non_linear_update(x: sympy.Matrix,
                      r: sympy.Matrix,
                      k: sympy.Matrix,
                      f: sympy.Matrix,
                      dt: float,
                      *args, **dargs) -> sympy.Matrix:
    """
    Non linear update equation to handle question 4
    @arg x is the previous state sys
    @arg r input before any feedback
    @arg k feedback matrix
    @arg f output equation given the state variables
    @returns next state
    """
    if k is not None:
        u = r - (k*x)
    else:
        u = r
    y = (r'y', x[0, 0])
    theta_1 = (r'\theta_1', x[1, 0])
    theta_2 = (r'\theta_2', x[2, 0])
    dot_y = (r'\doty', x[3, 0])
    dot_theta_1 = (r'\dot\theta_1', x[4, 0])
    dot_theta_2 = (r'\dot\theta_2', x[5, 0])
    u = ('u', u[0,0])
    dot_x = f.subs([
        theta_1, theta_2, y,
        dot_theta_1, dot_theta_2, dot_y,
        u
    ])
    new_x = sympy.N(x + (dt*dot_x))
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
        u = r - (k*x)
    else:
        u = r
    dx = A*x + B*u
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


def linear_output_with_observer(x: sympy.Matrix,
                                r: sympy.Matrix,
                                A: sympy.Matrix,
                                B: sympy.Matrix,
                                C: sympy.Matrix,
                                D: sympy.Matrix,
                                *args, **dargs) -> sympy.Matrix:
    """
    Linear output equation with observer,
    performs the observer update as well(linear)
    """
    return C*x + D*r
