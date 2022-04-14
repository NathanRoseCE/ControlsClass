from LatexTemplater.TemplateFilter import TemplateFilter
from .snippets.equations_of_motion import *
from .snippets.feedback import *
from .snippets.model import *
from .General import pre_process, plot
import numpy as np

def registrationInfo():
    return {
         KDesign.name: KDesign.filter,
         KEvaluationLinear.name: KEvaluationLinear.filter,
         KEvaluationNonLinear.name: KEvaluationNonLinear.filter
    }

          
class KDesign(TemplateFilter):
    name="design_k"

    @staticmethod
    def filter(vals_dict: str) -> str:
        vals_dict = pre_process(vals_dict)
        A, B, x = linearized_update_equation(evaluate_vals=True, **vals_dict)
        k, work = generate_k(A, B, **vals_dict)
        return work
   
class KEvaluationLinear(TemplateFilter):
    name = "eval_k_linear"
    
    @staticmethod
    def filter(vals_dict: str) -> str:
        vals_dict = pre_process(vals_dict)
        A, B, x = linearized_update_equation(evaluate_vals=True, **vals_dict)
        k, work = generate_k(A, B, **vals_dict)
        C = sympy.Matrix([[1,1,1,1,1,1]]) # output is distance from origin
        D = sympy.Matrix([[0]])
        duration = vals_dict["duration"]
        dt = vals_dict["dt"]
        x_0s = [
             sympy.Matrix(x_0) for x_0 in vals_dict["x_0s_linear"]
        ]
        output_names = [
             f"x_0 = {x_0}" for x_0 in vals_dict["x_0s_linear"]
        ]
        time_steps = np.arange(start=0, stop=duration, step=dt)
        inputs = [sympy.Matrix([[0]]) for t in time_steps]
        run_name = "sample"
        graph_location = f"resources/{run_name}.png"
        caption=" Linear analyis"
        outputs = [model_system(
             update=linear_update,
             output=linear_output,
             inputs=inputs,
             A=A, B=B, C=C, D=D, k=k, dt=dt, x_0=x_0
        ) for x_0 in x_0s]
        plot(time_steps,
             outputs,
             graph_location,
             run_name,
             output_names=output_names 
        )
        inst = TemplateCore.instance()
        return inst.filter(
            "image",
            [f"../{graph_location}", caption, f"fig:{run_name}"]
        )

class KEvaluationNonLinear(TemplateFilter):
    name = "eval_k_nonlinear"
    
    @staticmethod
    def filter(vals_dict: str) -> str:
        vals_dict = pre_process(vals_dict)
        total, output_str, M, little_f, big_F = equation_of_motion_sympy(evaluate_vals=True, **vals_dict)
        A, B, x = linearized_update_equation(evaluate_vals=True, **vals_dict)
        k, work = generate_k(A, B, **vals_dict)
        C = sympy.Matrix([[1,1,1,1,1,1]]) # output is distance from origin
        D = sympy.Matrix([[0]])
        duration = vals_dict["duration"]
        dt = vals_dict["dt"]
        x_0s = [
             sympy.Matrix(x_0) for x_0 in vals_dict["x_0s_nonlinear"]
        ]
        output_names = [
             f"x_0 = {x_0}" for x_0 in vals_dict["x_0s_nonlinear"]
        ]
        time_steps = np.arange(start=0, stop=duration, step=dt)
        inputs = [sympy.Matrix([[0]]) for t in time_steps]
        run_name = "nonlinear"
        graph_location = f"resources/{run_name}.png"
        caption="NonLinear analyis"
        outputs = []
        for x_0 in x_0s:
             outputs.append(model_system(
                  update=non_linear_update,
                  output=linear_output,
                  inputs=inputs,
                  f=total, C=C, D=D, k=k, dt=dt, x_0=x_0
             ))
        plot(time_steps,
             outputs,
             graph_location,
             run_name,
             output_names=output_names 
        )
        inst = TemplateCore.instance()
        return inst.filter(
            "image",
            [f"../{graph_location}", caption, f"fig:{run_name}"]
        )

