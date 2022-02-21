import numpy as np
import sympy
from LatexTemplater.TemplateCore import TemplateCore
from sympy import Matrix, eye, latex, simplify, roots, zeros
from typing import Iterable, Tuple

def eigenvalues(A: Matrix, show_work: bool=True) -> Tuple[str, Iterable[complex]]:
    """
    This function provides a method for calculating the eigenvalues of a matrix A
    it return a tuple of the string with work and a list of all the eigenvalues
    """
    #cannot use lambda as variable name as that is a key word for an anonymous function
    work = ""
    if show_work:
        work += r"\begin{equation}" + '\n'
        work += r"  \vert \lambda I - A \vert = 0" + '\n'
        work += r"\end{equation}" + '\n'
    l = sympy.symbols(r'\lambda')
    delta_l = simplify((eye(A.shape[0])*l) - A)
    det = simplify(delta_l.det())
    if show_work:
        work += r"\begin{equation}" + '\n'
        work += f"  det({latex(delta_l)}) = {latex(det)} = 0" + '\n'
        work += r"\end{equation}" + '\n'
    root_vals = roots(det)
    zeros = []
    for root, multiplicity in root_vals.items():
        zeros += [root for i in range(multiplicity)]
    inst = TemplateCore.instance() # this is just used for simple formatting
    if show_work:
        work += r"\begin{equation}" + '\n'
        work += r"  \lambda = " + f"{inst.filter('complexCsv', zeros)}\n"
        work += r"\end{equation}" + '\n'
    return work, zeros

def eigenvectors(A: Matrix, show_eigval_work: bool=True) -> Tuple[str, Iterable[complex]]:
    """
    This function provides a method for calculating the eigenvectors of a matrix,
    if show_eigval_work is set will include the work for finding the eigenvalues
    """
    work = ""
    eig_work, eig_vals = eigenvalues(A, show_eigval_work)
    if show_eigval_work:
        work += eig_work
    eig_multiplicity = {}
    for eig in eig_vals:
        if eig in eig_multiplicity:
            eig_multiplicity[eig] += 1
        else:
            eig_multiplicity[eig] = 1
    eig_vectors = []
    for eig, mult in eig_multiplicity.items():
        vector_work, vectors = _handle_multiplicity_eig(A, eig, mult)
        eig_vectors = list(vectors) + eig_vectors
        work += vector_work
    P, J = A.jordan_form()
    # cheating code
    # eig_vectors = [P.col(i) for i in range(A.shape[0])]
    return work, eig_vectors

def _handle_multiplicity_eig(A: Matrix, eig_val: complex, multiplicity: int) -> Tuple[str, Iterable[Matrix]]:
    """
    This function handles one group of eigenvalues with the same values
    returns the work and the 
    """
    vector_symbols = ", ".join([f'x_{i}' for i in range(A.shape[0])])
    symbols = list(sympy.symbols(vector_symbols))
    eig_vectors = []
    a_minus_lambda_i = simplify(A - (eye(A.shape[0])*eig_val))
    work = f"Solving for eigenvalue(s) of {eig_val}, with a multiplicity of {multiplicity}"
    print(work)
    print(f"A = {A}")
    print(f"A-li = {a_minus_lambda_i}")
    for i in range(multiplicity):
        power = multiplicity-i
        left = a_minus_lambda_i ** power
        print(f"{power} - {left}")
        eig_vec = Matrix([[x_i] for x_i in symbols])
        if np.all(np.matrix(left) == np.matrix(zeros(*left.shape))):
            work += r"\begin{equation}"
            work += r"  (A - \lambda i)^" + f"{power}x_{i} = 0"
            work += r"\end{equation}"
            work += r"\begin{equation}"
            work += f"  {latex(left)}{latex(eig_vec)} = 0"
            work += r"\end{equation}"
            result_vec = Matrix([[0] for _ in range(left.shape[0])])
            result_vec[0,0] = 1
            eig_vectors.append(result_vec)
            work += r"\begin{equation}"
            work += f"  x_{i} = {latex(result_vec)}"
            work += r"\end{equation}"
        elif i == 0:
            work += r"\begin{equation}"
            work += f"  {latex(left)}{latex(eig_vec)} = 0"
            work += r"\end{equation}"
            work += r"\begin{equation}"
            work += f"  {latex(left)}{latex(eig_vec)} = 0"
            work += r"\end{equation}"
            work += r"\begin{equation}"
            work += f"  {latex(left)}{latex(eig_vec)} = 0"
            work += r"\end{equation}"
            result = sympy.solve(left*eig_vec, symbols, particular=True)
            result_vec = sympy.zeros(len(symbols), 1)
            print(left*eig_vec)
            print(symbols)
            print(result)
            for j, x_i in enumerate(symbols):
                if x_i in result:
                    result_vec[j, 0] = result[x_i]
            eig_vectors.append(result_vec)
            work += r"\begin{equation}"
            work += f"  x_{i} = {latex(result_vec)}"
            work += r"\end{equation}"
        else:
            previous_eig_vector = eig_vectors[-1]
            work += r"\begin{equation}"
            work += r"  (A - \lambda i)^" + f"{power}{latex(previous_eig_vector)} = x_{i}"
            work += r"\end{equation}"
            work += r"\begin{equation}"
            work += f"{latex(left)}{latex(previous_eig_vector)} = x_{i}"
            work += r"\end{equation}"
            result = sympy.solve(left*previous_eig_vector - eig_vec, symbols, particular=True)
            result_vec = sympy.zeros(len(symbols), 1)
            for j, x_i in enumerate(symbols):
                result_vec[j, 0] = result[x_i]
            eig_vectors.append(result_vec)
            work += r"\begin{equation}"
            work += f"  x_{i} = {latex(result_vec)}"
            work += r"\end{equation}"
    inst = TemplateCore.instance()
    return (work, reversed(eig_vectors))
def _handle_multiplicity_eig_two(A: Matrix, eig_val: complex, multiplicity: int) -> Tuple[str, Iterable[Matrix]]:
    """
    This function handles one group of eigenvalues with the same values
    returns the work and the 
    """
    vector_symbols = ", ".join([f'x_{i}' for i in range(A.shape[0])])
    symbols = list(sympy.symbols(vector_symbols))
    eig_vectors = []
    a_minus_lambda_i = simplify(A - (eye(A.shape[0])*eig_val))
    work = f"Solving for eigenvalue(s) of {eig_val}, with a multiplicity of {multiplicity}"
    print(work)
    print(f"A = {A}")
    print(f"A-li = {a_minus_lambda_i}")
    for i in range(multiplicity):
        power = i+1
        left = a_minus_lambda_i ** power
        print(f"{power} - {left}")
        eig_vec = Matrix([[x_i] for x_i in symbols])
        if np.all(np.matrix(left) == np.matrix(zeros(*left.shape))):
            work += r"\begin{equation}"
            work += r"  (A - \lambda i)^" + f"{power}x_{i} = 0"
            work += r"\end{equation}"
            work += r"\begin{equation}"
            work += f"  {latex(left)}{latex(eig_vec)} = 0"
            work += r"\end{equation}"
            result_vec = Matrix([[0] for _ in range(left.shape[0])])
            result_vec[0,0] = 1
            eig_vectors.append(result_vec)
            work += r"\begin{equation}"
            work += f"  x_{i} = {latex(result_vec)}"
            work += r"\end{equation}"
            raise ValueError("uhhh")
        elif i == 0:
            work += r"\begin{equation}"
            work += f"  {latex(left)}{latex(eig_vec)} = 0"
            work += r"\end{equation}"
            work += r"\begin{equation}"
            work += f"  {latex(left)}{latex(eig_vec)} = 0"
            work += r"\end{equation}"
            work += r"\begin{equation}"
            work += f"  {latex(left)}{latex(eig_vec)} = 0"
            work += r"\end{equation}"
            result = sympy.solve(left*eig_vec, symbols, particular=True)
            result_vec = sympy.zeros(len(symbols), 1)
            print(left*eig_vec)
            print(symbols)
            print(result)
            for j, x_i in enumerate(symbols):
                if x_i in result:
                    result_vec[j, 0] = result[x_i]
            eig_vectors.append(result_vec)
            work += r"\begin{equation}"
            work += f"  x_{i} = {latex(result_vec)}"
            work += r"\end{equation}"
        else:
            previous_eig_vector = eig_vectors[-1]
            work += r"\begin{equation}"
            work += r"  (A - \lambda i)^" + f"{power}{latex(previous_eig_vector)} = x_{i}"
            work += r"\end{equation}"
            work += r"\begin{equation}"
            work += f"{latex(left)}{latex(previous_eig_vector)} = x_{i}"
            work += r"\end{equation}"
            result = sympy.solve(left*previous_eig_vector - eig_vec, symbols, particular=True)
            result_vec = sympy.zeros(len(symbols), 1)
            for j, x_i in enumerate(symbols):
                result_vec[j, 0] = result[x_i]
            eig_vectors.append(result_vec)
            work += r"\begin{equation}"
            work += f"  x_{i} = {latex(result_vec)}"
            work += r"\end{equation}"
    inst = TemplateCore.instance()
    return (work, reversed(eig_vectors))
    
def modal_matrix(A: Matrix, show_eigen_work: True) -> Matrix:
    work, vectors = eigenvectors(A, show_eigen_work)
    modal = Matrix([[vectors[row][column,0] for row in range(len(vectors))]
              for column in range(len(vectors))])
    work += "\n"
    work += r"\begin{equation}" + "\n"
    work += f"  V = {latex(modal)}"
    work += r"\end{equation}" + "\n"
    return work, modal
