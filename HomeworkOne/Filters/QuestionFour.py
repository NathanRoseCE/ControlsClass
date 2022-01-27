from LatexTemplater.TemplateFilter import TemplateFilter
from LatexTemplater.TemplateCore import TemplateCore
from typing import Dict, Callable, Iterable
import control
from control.xferfcn import ss2tf
import numpy as np
import sympy
from sympy import Matrix, shape, eye, latex, simplify
import logging

def registrationInfo() -> Dict[str, Callable[[any], str]]:
     return {
         StateSpace.name: StateSpace.filter,
         TransferFunction.name: TransferFunction.filter
     }
    
class StateSpace(TemplateFilter):
    name="FourSS"

    @staticmethod
    def filter(state: dict) -> str:
        A = state["A"]
        B = state["B"]
        C = state["C"]
        D = state["D"]
        inst = TemplateCore.instance()
        return inst.filter("ss", (A,B,C,D))

class TransferFunction(TemplateFilter):
    name="FourTF"

    @staticmethod
    def filter(state: dict) -> str:
        A = Matrix(state["A"])
        B = Matrix(state["B"])
        C = Matrix(state["C"])
        D = Matrix(state["D"])
        inst = TemplateCore.instance()

        # return inst.filter("eq", inst.filter("tf", ss2tf(A,B,C,D)))
        return inst.filter("eq", custom_ss2tf(A,B,C,D))

def custom_ss2tf(A: Matrix, B: Matrix, C: Matrix, D: Matrix) -> None:
     s = sympy.symbols('s')
     s_I = eye(shape(A)[0])*s
     manual_result = (C * (s_I-A).inv() * B) + D
     return latex(simplify(manual_result))
