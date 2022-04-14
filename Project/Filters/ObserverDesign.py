from LatexTemplater.TemplateFilter import TemplateFilter
from .snippets.equations_of_motion import *
from .snippets.observer import *
from .snippets.model import *
from .General import pre_process
import numpy as np
import matplotlib.pyplot as plt

def registrationInfo():
    return {
         LDesign.name: LDesign.filter
    }

class LDesign(TemplateFilter):
    name = "design_l"
    
    @staticmethod
    def filter(vals_dict: str) -> str:
        vals_dict = pre_process(vals_dict)
        A, B, x = linearized_update_equation(evaluate_vals=True, **vals_dict)
        C = sympy.Matrix(vals_dict["C"])
        l, work = generate_l(A, B, C, **vals_dict)
        return work
