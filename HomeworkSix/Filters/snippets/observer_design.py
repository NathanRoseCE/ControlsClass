from typing import Tuple, Iterable
import operator
import functools
import sympy
import random
# from ..General import *
# from .feedback import *


ROUND_TO=3
def latex_rounded(expr):
    return sympy.latex(expr.xreplace({n : round(n, ROUND_TO) for n in expr.atoms(sympy.Number)}))

def parse_eigenvalues(vals):
    eigs = []
    for val in vals:
        if not "imaginary" in val:
            eigs.append(
                val["real"]
            )
        else:
            eigs.append(
                val["real"] +
                (val["imaginary"]*1j)
            )
            eigs.append(
                val["real"] - 
                (val["imaginary"]*1j)
            )
        
    return eigs

def is_observable(A, C) -> bool:
    """
    checks to see if a system is observable given A and C, assumes
    A = 3x3
    C = 1x6
    """
    tmp =  C.col_join(C*A).col_join(C*(A**2))
    return tmp.det() != 0

def flip(matrix):
    flipped = []
    for i in range(len(matrix))[::-1]:
        flipped.append(matrix.row(i))
    return sympy.Matrix(flipped)


def generate_l(A: sympy.Matrix,
               B: sympy.Matrix,
               multi_C: sympy.Matrix,
               desired_eigenvalues: Iterable[float]) -> Tuple[sympy.Matrix, str]:
    """
    generates the feedback matrix, and returns the work needed to calculate itn
    """
    # k, work = generate_k(A=A,
    #                      B=B,
    #                      desired_controller_eigenvalues=desired_controller_eigenvalues,
    #                      **kwargs)
    # A = A - B*k
    # TODO: use method 2 on slide deck, much easier to program
    eigenvals = parse_eigenvalues(desired_eigenvalues)
    work_str = ""
    work_str += "The first goal will be to reduce the multi-output model to a single\n"
    work_str += "output model\n"

    assert multi_C.col_join(multi_C*A)[0:3,:].det() != 0
    
    for _ in range(10): # 10 tried then give up
        v = sympy.Matrix([[random.uniform(1, 2) for _ in range(2)]])
        if is_observable(A, v*multi_C):
            break
    assert is_observable(A, v*multi_C)
    work_str += r"\begin{equation}"+"\n"
    work_str += r"v = "+ latex_rounded(v)  +"\n"
    work_str += r"\end{equation}"+"\n"
    
    C = v*multi_C
    
    work_str += "the desired eigenvalues for the observer are: \n" 
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
    bar_alpha = flip(sympy.Matrix([[val] for val in bar_alpha]))
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
    # alpha.append(0) # doesnt include constant
    alpha = flip(sympy.Matrix([[val] for val in alpha]))
    work_str += "Desired Characteristic equation\n"
    work_str += r"\begin{equation}" + "\n"
    work_str += r"\alpha = " + latex_rounded(alpha) + "\n"
    work_str += r"\end{equation}" + "\n"

    bar_l = bar_alpha - alpha
    work_str += r"$\bar l$"+"\n"
    work_str += r"\begin{equation}"+"\n"
    work_str += r"  \bar l = \bar \alpha - \alpha = "+"\n"
    work_str += r"\end{equation}"+"\n"
    work_str += r"\begin{equation}"+"\n"
    work_str += f"  \\bar l = {latex_rounded(bar_alpha)} - \\\\{latex_rounded(alpha)} = \n"
    work_str += r"\end{equation}"+"\n"
    work_str += r"\begin{equation}"+"\n"
    work_str += f"  \\bar l = {latex_rounded(bar_l)}\n"
    work_str += r"\end{equation}"+"\n"

    # GOT HERE
    work_str += "Calculate P\n"
    work_str += r"\begin{equation}"+"\n"
    work_str += r" Q = P.T = "+"\n"
    work_str += r"  \begin{bmatrix}"+"\n"
    work_str += r"    (A.T)^2C.T & (A.T)C.T & C.T\\"+"\n"
    work_str += r"  \end{bmatrix}"+"\n"
    work_str += r"  \begin{bmatrix}"+"\n"
    work_str += r"    1 & 0 & 0 \\"+"\n"
    work_str += r"    \alpha_1 & 1 & 0 \\"+"\n"
    work_str += r"    \alpha_2 & \alpha_1 & 1 \\"+"\n"
    work_str += r"  \end{bmatrix}"+"\n"
    work_str += r"\end{equation}"
    alpha_1 = alpha[0]
    alpha_2 = alpha[1]
    alpha_3 = alpha[2]
    tmp_two = sympy.Matrix([
        [1, 0, 0],
        [alpha_1, 1, 0],
        [alpha_2, alpha_1, 1],
    ])
    tmp = ((A.T**2)*C.T).row_join(A.T*C.T).row_join(C.T)
    Q = tmp*tmp_two
    P = Q.T
    work_str += r"\begin{equation}"+"\n"
    work_str += f"  Q = {latex_rounded(tmp)}{latex_rounded(tmp_two)}"+"\n"
    work_str += r"\end{equation}"+"\n"
    work_str += r"\begin{equation}"+"\n"
    work_str += f"  Q = {latex_rounded(Q)}"+"\n"
    work_str += r"\end{equation}"+"\n"
    work_str += r"\begin{equation}"+"\n"
    work_str += r"  P = Q.T = " + f"{latex_rounded(P)}\n"
    work_str += r"\end{equation}"+"\n"

    l = P.inv() * bar_l
    work_str += r"\begin{equation}"+"\n"
    work_str += r"  l = P^{-1} \bar l  = " + latex_rounded(l) + "\n"
    work_str += r"\end{equation}"+"\n"

    L = l*v
    work_str += r"\begin{equation}"+"\n"
    work_str += r"  L = lv  = " + latex_rounded(L) + "\n"
    work_str += r"\end{equation}"+"\n"

    work_str += "To verify the equations use: eig($ A - LC$)\n"
    work_str += r"\begin{equation}"+"\n"
    work_str += r"  \vert \lambda - (A - LC) \vert  = " + latex_rounded((A-L*multi_C).charpoly()) + "\n"
    work_str += r"\end{equation}"+"\n"
    work_str += r"\begin{enumerate}"+"\n"
    for eig in (A - L*multi_C).eigenvals():
        work_str += r"\item $\lambda = " + latex_rounded(eig) + "$\n"
    work_str += r"\end{enumerate}"+"\n"
    
    return L, work_str
    
