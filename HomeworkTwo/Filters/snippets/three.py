from typing import Iterable, Tuple
from sympy import Matrix, latex, eye


def beta_equation_general() -> str:
    return r"f(\lambda) = \beta_0 + \beta_1\lambda + \beta_2\lambda^2"
                       
def beta_equation(eig_vals: list) -> Tuple[Matrix,Matrix]:
    """
    gets the matrix form of the equations above for a 3x3 and given eigenvalues.
    Assumes no multiplicity and f is inverse
    """
    values = []
    system = []
    for eig_val in eig_vals:
        values.append(
            pow(eig_val, -1)
        )
        system.append(
            [pow(eig_val, i) for i in range(len(eig_vals))]
        )
    return Matrix(values), Matrix(system)

def bmatrix() -> str:
    return r"\begin{bmatrix}\beta_0 \\ \beta_1 \\ \beta_2 \end{bmatrix}"

def beta_equation_str(eig_vals) -> str:
    values, system = beta_equation(eig_vals)
    return (f"{latex(values)} = {latex(system)}" + r"^{-1}" +
            bmatrix()
            )
def solved_beta_equation_str(eig_vals) -> str:
    values, system = beta_equation(eig_vals)
    solved = system.inv() * values
    return (
        bmatrix() + f" = {latex(solved)}" 
    )

def beta_values(eig_vals) -> Iterable[float]:
    values, system = beta_equation(eig_vals)
    solved = system.inv() * values
    return [solved[i, 0] for i in range(3)]

def final_answer(eig_vals, A) -> str:
    A = Matrix(A)
    I = eye(A.shape[0])
    beta_0, beta_1, beta_2 = beta_values(eig_vals)
    return (beta_0*I) + (beta_1*A) + (beta_2*A*A)
