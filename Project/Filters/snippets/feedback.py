from typing import Tuple, Iterable
import operator
import functools
import sympy
from sympy import Number

ROUND_TO=3
def latex_rounded(expr):
    return sympy.latex(expr.xreplace({n : round(n, ROUND_TO) for n in expr.atoms(Number)}))

def generate_k(A: sympy.Matrix,
               B: sympy.Matrix,
               desired_controller_eigenvalues: Iterable[float],
               **kwargs) -> Tuple[sympy.Matrix, str]:
    """
    generates the feedback matrix, and returns the work needed to calculate it
    """
    eigenvals = desired_controller_eigenvalues
    work_str = ""
    work_str += "the desired eigenvalues after feedback are: \n" 
    work_str += r"\begin{equation}"+"\n"
    work_str += r"\lambda = "+', '.join([str(eig) for eig in eigenvals])+"\n"
    work_str += r"\end{equation}"+"\n"
    
    s_lambda = sympy.symbols(r'\lambda')
    d_characteristic_equation = functools.reduce(
        lambda a, b: a*b, 
        [(s_lambda - eigen_val) for eigen_val in eigenvals]
    )
    vals = [(s_lambda - eigen_val) for eigen_val in eigenvals]
    d_characteristic_equation = sympy.expand(d_characteristic_equation)
    work_str += "Desired Characteristic equation\n"
    work_str += r"\begin{equation}" + "\n"
    work_str += r"\Delta_d(\lambda) = " + latex_rounded(d_characteristic_equation) + "\n"
    work_str += r"\end{equation}" + "\n"
    bar_alpha = sympy.Poly(d_characteristic_equation, s_lambda).coeffs()[1:]
    bar_alpha = sympy.Matrix([[val for val in bar_alpha]])
    work_str += "Desired Characteristic equation\n"
    work_str += r"\begin{equation}" + "\n"
    work_str += r"\bar \alpha = " + latex_rounded(bar_alpha) + "\n"
    work_str += r"\end{equation}" + "\n"

    characteristic_equation = A.charpoly()
    work_str += "Desired Characteristic equation\n"
    work_str += r"\begin{equation}" + "\n"
    work_str += r"\Delta_d(\lambda) = " + latex_rounded(characteristic_equation) + "\n"
    work_str += r"\end{equation}" + "\n"
    alpha = characteristic_equation.coeffs()[1:]
    alpha.append(0) # doesnt include constant
    alpha = sympy.Matrix([[val for val in alpha]])
    work_str += "Desired Characteristic equation\n"
    work_str += r"\begin{equation}" + "\n"
    work_str += r"\alpha = " + latex_rounded(alpha) + "\n"
    work_str += r"\end{equation}" + "\n"

    bar_k = bar_alpha - alpha
    work_str += r"$\bar k$"+"\n"
    work_str += r"\begin{equation}"+"\n"
    work_str += r"  \bar k = \bar \alpha - \alpha = "+"\n"
    work_str += r"\end{equation}"+"\n"
    work_str += r"\begin{equation}"+"\n"
    work_str += f"  \\bar k = {latex_rounded(bar_alpha)} - \\\\{latex_rounded(alpha)} = \n"
    work_str += r"\end{equation}"+"\n"
    work_str += r"\begin{equation}"+"\n"
    work_str += f"  \\bar k = {latex_rounded(bar_k)}\n"
    work_str += r"\end{equation}"+"\n"

    work_str += "Calculate P\n"
    work_str += r"\begin{equation}"+"\n"
    work_str += r" Q = P^{-1} = "+"\n"
    work_str += r"  \begin{bmatrix} B & AB & A^2B \end{bmatrix}"+"\n"
    work_str += r"  \begin{bmatrix}"+"\n"
    work_str += r"    1 & \alpha_1 & \alpha_2 & \alpha_3 & \alpha_4 & \alpha_5\\"+"\n"
    work_str += r"    0 & 1 & \alpha_1 & \alpha_2 & \alpha_3 & \alpha_4\\"+"\n"
    work_str += r"    0 & 0 & 1 & \alpha_1 & \alpha_2 & \alpha_3\\"+"\n"
    work_str += r"    0 & 0 & 0 & 1 & \alpha_1 & \alpha_2\\"+"\n"
    work_str += r"    0 & 0 & 0 & 0 & 1 & \alpha_1\\"+"\n"
    work_str += r"    0 & 0 & 0 & 0 & 0 & 1\\"+"\n"
    work_str += r"  \end{bmatrix}"+"\n"
    work_str += r"\end{equation}"
    alpha_1 = alpha[0]
    alpha_2 = alpha[1]
    alpha_3 = alpha[2]
    alpha_4 = alpha[3]
    alpha_5 = alpha[4]
    tmp_two = sympy.Matrix([
        [1, alpha_1, alpha_2, alpha_3, alpha_4, alpha_5],
        [0, 1, alpha_1, alpha_2, alpha_3, alpha_4],
        [0, 0, 1, alpha_1, alpha_2, alpha_3],
        [0, 0, 0, 1, alpha_1, alpha_2],
        [0, 0, 0, 0, 1, alpha_1],
        [0, 0, 0, 0, 0, 1]
    ])
    tmp = B.row_join(A*B).row_join((A**2)*B).row_join((A**3)*B).row_join((A**4)*B).row_join((A**5)*B)
    Q = tmp*tmp_two
    P = Q.inv()
    work_str += r"\begin{equation}"+"\n"
    work_str += f"  Q = {latex_rounded(tmp)}{latex_rounded(tmp_two)}"+"\n"
    work_str += r"\end{equation}"+"\n"
    work_str += r"\begin{equation}"+"\n"
    work_str += f"  Q = {latex_rounded(Q)}"+"\n"
    work_str += r"\end{equation}"+"\n"
    work_str += r"\begin{equation}"+"\n"
    work_str += r"  P = Q^{-1} = " + f"{latex_rounded(P)}\n"
    work_str += r"\end{equation}"+"\n"

    k = bar_k * P
    work_str += r"\begin{equation}"+"\n"
    work_str += r"  k = \bar k P = " + latex_rounded(k) + "\n"
    work_str += r"\end{equation}"+"\n"
    
    return sympy.Matrix(), work_str
    
