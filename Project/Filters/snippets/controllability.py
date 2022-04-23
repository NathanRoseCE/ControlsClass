import sympy
from ..General import *
from typing import Tuple

def is_controllable(A: sympy.Matrix, B: sympy.Matrix) -> Tuple[bool, str]:
    """
    Quick function to check if the system is controllable
    """
    work_str = "Controllability of the system:\n"
    work_str += r"\begin{equation}" + "\n"
    work_str += r"  \begin{bmatrix}" + "\n"
    work_str += r"    B & AB & A^2B & A^3B & A^4B & A^5B" + "\n"
    work_str += r"  \end{bmatrix}" + "\n"
    work_str += r"\end{equation}" + "\n"
    joined_matrix = B.row_join(A*B).row_join(A**2*B).row_join(A**3*B).row_join(A**4*B).row_join(A**5*B)
    work_str += r"\begin{equation}" + "\n"
    work_str += latex_rounded(joined_matrix) + "\n"
    work_str += r"\end{equation}" + "\n"
    if joined_matrix.det() != 0:
        work_str += "The determinate is non-zero thus the system is controllable\n"
    else:
        work_str += "The determinate is zero thus the system is not controllable\n"
    return joined_matrix.det() != 0, work_str
    


def is_observable(A: sympy.Matrix, C: sympy.Matrix) -> Tuple[bool, str]:
    """
    Quick function to check if the system is controllable
    """
    work_str = "Observability of the system:\n"
    work_str += r"\begin{equation}" + "\n"
    work_str += r"  \begin{bmatrix}" + "\n"
    work_str += r"    C \\ CA \\ CA^2 \\ CA^3 \\ CA^4 \\ CA^5" + "\n"
    work_str += r"  \end{bmatrix}" + "\n"
    work_str += r"\end{equation}" + "\n"
    joined_matrix = C.col_join(C*A)
    work_str += r"\begin{equation}" + "\n"
    work_str += latex_rounded(joined_matrix) + "\n"
    work_str += r"\end{equation}" + "\n"
    if joined_matrix.det() != 0:
        work_str += "The determinate is non-zero thus the system is observable\n"
    else:
        work_str += "The determinate is zero thus the system is not observable\n"
    return joined_matrix.det() != 0, work_str
    


