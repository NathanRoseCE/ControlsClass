import sympy
from sympy import eye, shape, simplify, inverse_laplace_transform

def sI_A(A: sympy.Matrix):
    """
    a simplified function to handle sI-A for any A
    """
    s = sympy.symbols('s')
    s_I = eye(shape(A)[0])*s
    return simplify(s_I-A)

def stm_matrix(A: sympy.Matrix):
    """
    gets the state transition matrix given a STM
    """
    # this is accomplished by taking the inverse laplace of
    # (sI -A)^{-1}
    s, t = sympy.symbols('s, t')
    return sympy.exp(A*t)


def zero_input_response(A: sympy.Matrix, x_0: sympy.Matrix):
    """
    gets the zero input response of thes system
    """
    # the zero input response is just the stm times the initial state
    return stm_matrix(A)*x_0
    
def zero_state_response(A: sympy.Matrix, x_0: sympy.Matrix):
    """
    gets the zero input response of thes system
    """
    # the zero input response is just the stm times the initial state
    return stm_matrix(A)*x_0
   
def _get_integrand(A: sympy.Matrix, B: sympy.Matrix):
    """
    the integrand of the zero state response function
    """
    stm = STM_laplace_inverse(A) # from problem 1
    t, tau = symbols('t, ' + r'\tau')
    u = exp(2*t)
    return simplify((stm.subs(t, t-tau) * B.subs(t, tau) * u.subs(t, tau)))
