import sympy
from ..General import *
from typing import Tuple

def transfer_function(A: sympy.Matrix, B: sympy.Matrix, C: sympy.Matrix) -> Tuple[sympy.Matrix, str]:
    """
    Does the work for calculating the transfer matrix of a system
    """
    work_str = ""
    work_str += r"\begin{equation}"+"\n"
    work_str += r"G(s) = C(sI-A)^{-1}B + D"+"\n"
    work_str += r"\end{equation}"+"\n"

    s = sympy.symbols('s')    
    result = C * (s*sympy.eye(6) - A).inv() * B
    work_str += r"\begin{equation}"+"\n"
    work_str += r"G(s) = " + latex_rounded(result) + "\n"
    work_str += r"\end{equation}"+"\n"

    return result, work_str
