from LatexTemplater.TemplateFilter import TemplateFilter
from .snippets.equations_of_motion import *
from .snippets.feedback import *
from .General import pre_process

def registrationInfo():
     return {
         K_Design.name: K_Design.filter
     }
class K_Design(TemplateFilter):
    name="design_k"

    @staticmethod
    def filter(vals_dict: str) -> str:
        vals_dict = pre_process(vals_dict)
        A, B, x = linearized_update_equation(evaluate_vals=True, **vals_dict)
        k, work = generate_k(A, B, **vals_dict)
        return work
