from LatexTemplater.TemplateFilter import TemplateFilter
from LatexTemplater.TemplateCore import TemplateCore
from typing import Dict, Callable, Tuple
from sympy import latex, Matrix
from .snippets.two_a import *
from .snippets.two_b import *

def registrationInfo():
     return {
          Two_A.name: Two_A.filter,
          Two_B.name: Two_B.filter,
          Two_C.name: Two_C.filter
     }

class Two_A(TemplateFilter):
    name="two_a"

    @staticmethod
    def filter(system) -> str:
         system, x_0 = system
         A = Matrix(system["A"])
         B = Matrix(system["B"])
         x_0 = Matrix(x_0)
         inst = TemplateCore.instance()
         equation = inst.filter(
              "eq", r"x(t) = STM(t)x_0"
         )
         solved_equation = inst.filter(
              "eq", "x(t) =" + latex(zero_input_equation(A, x_0))
         )
         return equation + solved_equation

class Two_B(TemplateFilter):
     name = "two_b"

     @staticmethod
     def filter(system) -> str:
          A = Matrix(system["A"])
          B = Matrix(system["B"])
          inst = TemplateCore.instance()
          equation = inst.filter(
               "eq", r"x_{zs}(t) = \int_{t_0}^t \Phi(t,\tau)B(\tau)u(\tau)d\tau"
          )
          equation_subbed = inst.filter(
               "eq", r"x_{zs}(t) = \int_0^t" + latex(get_integrand(A,B)) + r"d\tau"
          )
          solved_equation = inst.filter(
               "eq", r"x_{zs}(t) = " + latex(zero_state(A, B))
          )
          return equation + equation_subbed + solved_equation

class Two_C(TemplateFilter):
     name = "two_c"

     @staticmethod
     def filter(system) -> str:
         system, x_0 = system
         A = Matrix(system["A"])
         B = Matrix(system["B"])
         x_0 = Matrix(x_0)
         zero_input_eq = zero_input_equation(A, x_0)
         zero_state_eq = zero_state(A, B)
         inst = TemplateCore.instance()
         return inst.filter(
              "eq",
              ("x(t) = " +
               latex(simplify(zero_input_eq+zero_state_eq)))
         )
