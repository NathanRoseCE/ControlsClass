from LatexTemplater.TemplateFilter import TemplateFilter
from .snippets.equations_of_motion import *
from .General import pre_process
def registrationInfo():
    return {
        NonlinearSymbolic.name: NonlinearSymbolic.filter,
        NonlinearEvaluated.name: NonlinearEvaluated.filter,
        LinearSymbolic.name: LinearSymbolic.filter,
        LinearEvaluated.name: LinearEvaluated.filter
     }
class NonlinearSymbolic(TemplateFilter):
    name="nonlinear_equation_symbolic"

    @staticmethod
    def filter(vals_dict: str) -> str:
        vals_dict = pre_process(vals_dict)
        return (
            equations_of_motion_nonlinear_str(evaluate_vals=False, **vals_dict) + "\n"+
            "This is unreadable\n"
        )
            

class NonlinearEvaluated(TemplateFilter):
    name="nonlinear_equation_evaluated"

    @staticmethod
    def filter(vals_dict: str) -> str:
        vals_dict = pre_process(vals_dict)
        return equations_of_motion_nonlinear_str(evaluate_vals=True, **vals_dict)
    
class LinearSymbolic(TemplateFilter):
    name="linear_equation_symbolic"

    @staticmethod
    def filter(vals_dict: str) -> str:
        return linearized_update_equation_str(evaluate_vals=False)
    
class LinearEvaluated(TemplateFilter):
    name="linear_equation_evaluated"

    @staticmethod
    def filter(vals_dict: str) -> str:
        vals_dict = pre_process(vals_dict)
        return linearized_update_equation_str(evaluate_vals=True, **vals_dict)
    
