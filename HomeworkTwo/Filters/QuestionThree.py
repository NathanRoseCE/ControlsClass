from LatexTemplater.TemplateFilter import TemplateFilter
from LatexTemplater.TemplateCore import TemplateCore
from typing import Dict, Callable, Tuple
from sympy import latex
from .snippets.one_a import *

def registrationInfo():
    return {
        ThreeA.name: ThreeA.filter
    }

class ThreeA(TemplateFilter):
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

