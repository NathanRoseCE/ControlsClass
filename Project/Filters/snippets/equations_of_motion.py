from typing import Tuple, Iterable
from functools import cache
import sympy
import functools
from sympy import Matrix as Matrix
from sympy import cos, sin
from LatexTemplater.TemplateCore import TemplateCore

from frozendict import frozendict

def freezeargs(func):
    """Transform mutable dictionnary
    Into immutable
    Useful to be compatible with cache
    """

    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        args = tuple([frozendict(arg) if isinstance(arg, dict) else arg for arg in args])
        kwargs = {k: frozendict(v) if isinstance(v, dict) else v for k, v in kwargs.items()}
        return func(*args, **kwargs)
    return wrapped

def state_symbols() -> Iterable[sympy.Symbol]:
    return sympy.symbols(
        r'y, \theta_1, \theta_2, \doty, \dot\theta_1, \dot\theta_2, u'
    )

# @freezeargs
# @cache
def equation_of_motion_sympy(evaluate_vals:bool=False,
                             *args, **dargs) -> Tuple[Matrix, str, Matrix, Matrix, Matrix]:
    """
    gets the sympy matrix
    returns:
      total, evaluted_vals_str, m, little_F, big_F
    """
    evaluated_vals_str = ""
    if evaluate_vals:
        m_c = dargs["m_c"]
        m_1 = dargs["m_1"]
        m_2 = dargs["m_2"]
        l_1 = dargs["l_1"]
        l_2 = dargs["l_2"]
        g = dargs["g"]
        d_1 = dargs["d_1"]
        d_2 = dargs["d_2"]
        d_3 = dargs["d_3"]
        evaluated_vals_str += "For this, I assumed: \n"
        evaluated_vals_str += r"\begin{enumerate}"
        for name, val in [("m_c", m_c),
                          ("m_1", m_c), 
                          ("m_2", m_c), 
                          ("l_1", m_c), 
                          ("l_2", m_c), 
                          ("g", m_c), 
                          ("d_1", m_c), 
                          ("d_2", m_c), 
                          ("d_3", m_c)]:
            evaluated_vals_str +=r"\item " + f"${name} = {val}$\n"
        evaluated_vals_str += r"\end{enumerate}"
        
    else:
        m_c, m_1, m_2, l_1, l_2, g, d_1, d_2, d_3 = sympy.symbols(r'm_c, m_1, m_2, l_1, l_2, g, d_1, d_2, d_3')
        
    y, theta_1, theta_2, dot_y, dot_theta_1, dot_theta_2, u = state_symbols()
    M = Matrix([
        [m_c+m_1+m_2,                 l_1*(m_1+m_2)*cos(theta_1),       m_2*l_2*cos(theta_2)],
        [l_1*(m_1+m_2)*cos(theta_1),  l_1*l_1*(m_1+m_2),                l_1*l_2*m_2*cos(theta_1-theta_2)],
        [l_2*m_2*cos(theta_2),        l_1*l_2*m_2*cos(theta_1-theta_2), l_2*l_2*m_2]
    ])
    little_f = (
        Matrix([
            [l_1*(m_1+m_2)*(dot_theta_1**2)*sin(theta_1) + m_2*l_2*(dot_theta_2**2)*sin(theta_2)],
            [-l_1*l_2*m_2*(dot_theta_2**2)*sin(theta_1-theta_2) + g*(m_1+m_2)*l_1*sin(theta_1)],
            [l_1*l_2*m_2*(dot_theta_1**2)*sin(theta_1-theta_2) + g*l_2*m_2*sin(theta_2)],
        ]) - Matrix([
            [d_1*dot_y],
            [d_2*dot_theta_1],
            [d_3*dot_theta_2]
        ]) + Matrix([
            [u],
            [0],
            [0]
        ])
    )
    little_f = sympy.simplify(little_f)
    big_F = M.inv() * little_f
    big_F = sympy.simplify(big_F)
    total = big_F.row_insert(0, Matrix([[dot_y]]))
    total = total.row_insert(0, Matrix([[dot_theta_1]]))
    total = total.row_insert(0, Matrix([[dot_theta_2]]))
    return total, evaluated_vals_str, M, little_f, big_F
    
    

def equations_of_motion_nonlinear_str(*args, **dargs) -> str:
    """
    generates the equations of motion, either as a latex string that can be printed(for the report)
    or as a lambda that can be used in simulation
    """
    total, output_str, M, little_f, big_F = equation_of_motion_sympy(*args, **dargs)
    return (
        output_str+"\n"+
        r"% generated equation"+"\n"
        r"\begin{equation}"+"\n"
        r"M = " + sympy.latex(M)+"\n"
        r"\end{equation}"+"\n"
        r"\begin{equation}"+"\n"
        r"f = " + sympy.latex(little_f)+"\n"
        r"\end{equation}"+"\n"
        r"\begin{equation}"+"\n"
        r"F = " + sympy.latex(big_F)+"\n"
        r"\end{equation}"+"\n"
        r"\begin{equation}"+"\n"+
        r"  \dot x = \frac d {dt} \begin{bmatrix} y \\ \dot y \end{bmatrix} = "+"\n"+
        sympy.latex(total)+"\n"+
        r"\end{equation}"
    ).replace(r'\\', r'\\'+'\n')

# @cache
def linearized_update_equation(*args, **dargs) -> Tuple[Matrix, Matrix, Matrix]:
    """
    gets the A, B, and x matrix for the linearized system
    """
    def gradient(scalar_function, variables):
        matrix_scalar_function = Matrix([scalar_function])
        return matrix_scalar_function.jacobian(variables)
    
    total, output_str, M, little_f, big_F = equation_of_motion_sympy(*args, **dargs)
    y, theta_1, theta_2, dot_y, dot_theta_1, dot_theta_2, u = state_symbols()
    A = gradient(total, [y, theta_1, theta_2, dot_y, dot_theta_1, dot_theta_2])
    B = gradient(total, [u])
    A = A.evalf(subs={
        y:0,
        theta_1:0,
        theta_2:0,
        dot_y:0,
        dot_theta_1:0,
        dot_theta_2:0
    })
    B = B.evalf(subs={
        y:0,
        theta_1:0,
        theta_2:0,
        dot_y:0,
        dot_theta_1:0,
        dot_theta_2:0
    })
    inst = TemplateCore.instance()
    x = sympy.Matrix([
        [y],
        [theta_1],
        [theta_2],
        [dot_y],
        [dot_theta_1],
        [dot_theta_2]
    ])
    return A, B, x

def linearized_update_equation_str(*args, **dargs) -> str:
    """
    linearized version of the update equation
    """
    A, B, x = linearized_update_equation(*args, **dargs)
    return (
        r"\begin{equation}"+"\n"+
        r" \dot x = "+sympy.latex(A)+sympy.latex(x)+" + "+sympy.latex(B)+"u\n"+
        r"\end{equation}"+"\n"
    )
