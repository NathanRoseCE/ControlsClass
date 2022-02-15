from LatexTemplater.TemplateFilter import TemplateFilter
from LatexTemplater.TemplateCore import TemplateCore
from typing import Dict, Callable, Tuple
from sympy import latex
from .snippets.eigen import *

def registrationInfo():
     return {
         One_System.name: One_System.filter,
         One_A.name: One_A.filter,
         One_B.name: One_B.filter
    }

class One_System(TemplateFilter):
    name = "one_system"

    @staticmethod
    def filter(system):
        A = Matrix(system["A"])
        return A

class One_A(TemplateFilter):
    name = "one_a"

    @staticmethod
    def filter(system):
        inst = TemplateCore.instance()
        A = inst.filter("one_system", system)
        eigen_work, eigen_vals = eigenvalues(A)
        return eigen_work

class One_B(TemplateFilter):
    name = "one_b"

    def filter(system):
        inst = TemplateCore.instance()
        A = inst.filter("one_system", system)
        work, V = modal_matrix(A, show_eigen_work=False)
        print(V)
        work += r"\begin{equation}"
        work += r"  J = V^{-1}AV = " + f"{latex(V.inv())}{latex(A)}{latex(V)}"
        work += r"\end{equation}"
        work += r"\begin{equation}"
        work += r"  J = " + f"{latex(V.inv()*A*V)}"
        work += r"\end{equation}"
        return work
