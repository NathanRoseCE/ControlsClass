from LatexTemplater.TemplateFilter import TemplateFilter
from LatexTemplater.TemplateCore import TemplateCore
from typing import Dict, Callable, Tuple
from sympy import latex
from .snippets.two_a import *

def registrationInfo():
     return {
         One_System.name: One_System.filter,
         One_A_Equation.name: One_A_Equation.filter,
         OneA.name: OneA.filter,
    }

class Two_A(TemplateFilter):
    name="two_a"

    @staticmethod
    def filter(system) -> Tuple:
        A = system["A"]
        B = system["B"]
        return A, B
