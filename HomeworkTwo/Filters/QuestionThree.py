from LatexTemplater.TemplateFilter import TemplateFilter
from LatexTemplater.TemplateCore import TemplateCore
from typing import Dict, Callable, Tuple
from sympy import latex
from .snippets.three import *
from .snippets.one_a import *

def registrationInfo():
    return {
        ThreeA.name: ThreeA.filter,
        ThreeB.name: ThreeB.filter
    }

class ThreeA(TemplateFilter):
    name="three_inverse"

    @staticmethod
    def filter(A) -> str:
        inst = TemplateCore.instance()
        eig_vals = inst.filter("eig_vals", A)
        final_str = inst.filter("eq", beta_equation_general()) + "\n"
        final_str += inst.filter("eq", beta_equation_str(eig_vals)) + "\n"
        final_str += inst.filter("eq", solved_beta_equation_str(eig_vals)) + "\n"
        final_str += inst.filter("eq", r"A^{-1} = " + latex(final_answer(eig_vals, A)))
        return final_str

class ThreeB(TemplateFilter):
    name="three_laplace_inv"
    
    @staticmethod
    def filter(A) -> str:
        inst = TemplateCore.instance()
        A = Matrix(A)
        result = STM_laplace_inverse(A)
        final_ans = inst.filter("eq",
                                inst.filter("laplace_inv",
                                            r"(sI-A)^{-1}") + 
                                " = " + latex(simplify(result)))
        return final_ans
