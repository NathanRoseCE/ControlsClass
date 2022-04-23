from LatexTemplater.TemplateFilter import TemplateFilter
from .snippets.equations_of_motion import *
from .snippets.transfer_function import *
from .snippets.controllability import *
from .General import pre_process

def registrationInfo():
    return {
        NonlinearSymbolic.name: NonlinearSymbolic.filter,
        NonlinearEvaluated.name: NonlinearEvaluated.filter,
        LinearSymbolic.name: LinearSymbolic.filter,
        LinearEvaluated.name: LinearEvaluated.filter,
        TransferFunction.name: TransferFunction.filter,
        Controllability.name: Controllability.filter,
        Observability.name: Observability.filter
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
    
class TransferFunction(TemplateFilter):
    name="transfer_function"

    @staticmethod
    def filter(vals_dict: str) -> str:
        A, B, x = linearized_update_equation(evaluate_vals=True, **vals_dict)
        C = sympy.Matrix(vals_dict["C"])
        tf, work = transfer_function(A=A, B=B, C=C)
        return work

class Controllability(TemplateFilter):
    name="controllable"

    @staticmethod
    def filter(vals_dict) -> str:
        A, B, x = linearized_update_equation(evaluate_vals=True, **vals_dict)
        yay_nay, work = is_controllable(A, B)
        return work
        
        
class Observability(TemplateFilter):
    name="observable"

    @staticmethod
    def filter(vals_dict) -> str:
        A, B, x = linearized_update_equation(evaluate_vals=True, **vals_dict)
        C = sympy.Matrix(vals_dict["C"])
        yay_nay, work = is_observable(A, C)
        return work
