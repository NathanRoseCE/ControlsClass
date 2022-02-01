from LatexTemplater.TemplateFilter import TemplateFilter
from LatexTemplater.TemplateCore import TemplateCore
from typing import Dict, Callable, Tuple
from sympy import latex
from .snippets.one_a import *

def registrationInfo():
     return {
         One_System.name: One_System.filter,
         One_A_Equation.name: One_A_Equation.filter,
         OneA.name: OneA.filter,
    }

class One_System(TemplateFilter):
    name="one_system"

    @staticmethod
    def filter(system) -> Tuple:
        A = system["A"]
        B = system["B"]
        return A, B

class One_A_Equation(TemplateFilter):
    name="one_system_eq"

    @staticmethod
    def filter(system) -> str:
        inst = TemplateCore.instance()
        return inst.filter("state_update",
                           inst.filter("one_system",
                                       system))
    
class OneA(TemplateFilter):
    name="one_laplace_inv"

    @staticmethod
    def filter(val: str) -> str:
        inst = TemplateCore.instance()
        A, B = inst.filter("one_system", val)
        result = STM_laplace_inverse(np.matrix(A))
        return inst.filter("eq",
                           inst.filter("laplace_inv",
                                       r"(sI-A)^{-1}") + 
                           " = " + latex(result))

