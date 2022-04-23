from LatexTemplater.TemplateFilter import TemplateFilter
from .snippets.equations_of_motion import *
from .snippets.observer import *
from .snippets.feedback import *
from .snippets.model import *
from .General import pre_process
import numpy as np
import matplotlib.pyplot as plt

def registrationInfo():
    return {
        LDesign.name: LDesign.filter,
        LEvaluationLinear.name: LEvaluationLinear.filter,
        LEvaluationWithKLinear.name: LEvaluationWithKLinear.filter,
        LEvaluationNonLinear.name: LEvaluationNonLinear.filter
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

class LEvaluationLinear(TemplateFilter):
    name = "eval_l_linear"
    
    @staticmethod
    def filter(vals_dict: str) -> str:
        vals_dict = pre_process(vals_dict)
        A, B, x = linearized_update_equation(evaluate_vals=True, **vals_dict)
        C = sympy.Matrix(vals_dict["C"])
        l, work = generate_l(A, B, C, **vals_dict)
        k, work = generate_k(A, B, **vals_dict)
        D = sympy.Matrix([[0],[0],[0]])
        duration = vals_dict["duration"]
        dt = vals_dict["dt"]
        x_0 = sympy.Matrix(vals_dict["x_0_linear_est_sys"])
        x_0_est = sympy.Matrix(vals_dict["x_0_linear_est_est"])
        output_names = [
            "system state",
            "estimated system state"
        ]
        time_steps = np.arange(start=0, stop=duration, step=dt)
        inputs = [sympy.Matrix([[0]]) for t in time_steps]
        run_name = "estimator-linear"
        graph_location = f"resources/{run_name}.png"
        caption="Estimator in Linear performance"
        outputs = model_system(
            update=observer_update_wrapper,
            output=observer_output_wrapper,
            system_update=linear_update,
            system_output=linear_output,
            observer_update=observer_update,
            inputs=inputs,
            A=A, B=B, C=C, D=D, L=l, dt=dt, x_0=(x_0, x_0_est)
        )
        true_outputs = []
        outputs = [[row[i] for row in outputs] for i in range(len(outputs[0]))]
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

class LEvaluationWithKLinear(TemplateFilter):
    name = "eval_l_with_k_linear"
    
    @staticmethod
    def filter(vals_dict: str) -> str:
        vals_dict = pre_process(vals_dict)
        A, B, x = linearized_update_equation(evaluate_vals=True, **vals_dict)
        C = sympy.Matrix(vals_dict["C"])
        l, work = generate_l(A, B, C, **vals_dict)
        k, work = generate_k(A, B, **vals_dict)
        D = sympy.Matrix([[0],[0],[0]])
        duration = vals_dict["duration"]
        dt = vals_dict["dt"]
        x_0 = sympy.Matrix(vals_dict["x_0_linear_est_sys"])
        x_0_est = sympy.Matrix(vals_dict["x_0_linear_est_est"])
        output_names = [
            "system state",
            "estimated system state"
        ]
        time_steps = np.arange(start=0, stop=duration, step=dt)
        inputs = [sympy.Matrix([[0]]) for t in time_steps]
        run_name = "estimator-linear-with-k"
        graph_location = f"resources/{run_name}.png"
        caption="Estimator in Linear performance"
        outputs = model_system(
            update=observer_update_wrapper,
            output=observer_output_wrapper,
            system_update=linear_update,
            system_output=linear_output,
            observer_update=observer_update,
            inputs=inputs,
            A=A, B=B, C=C, D=D, L=l, k=k, dt=dt, x_0=(x_0, x_0_est)
        )
        outputs = [[row[i] for row in outputs] for i in range(len(outputs[0]))]
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
    
class LEvaluationNonLinear(TemplateFilter):
    name = "eval_l_nonlinear"
    
    @staticmethod
    def filter(vals_dict: str) -> str:
        vals_dict = pre_process(vals_dict)
        A, B, x = linearized_update_equation(evaluate_vals=True, **vals_dict)
        total, output_str, M, little_f, big_F = equation_of_motion_sympy(evaluate_vals=True, **vals_dict)
        C = sympy.Matrix(vals_dict["C"])
        l, work = generate_l(A, B, C, **vals_dict)
        k, work = generate_k(A, B, **vals_dict)
        D = sympy.Matrix([[0],[0],[0]])
        duration = vals_dict["duration"]
        dt = vals_dict["dt"]
        x_0 = sympy.Matrix(vals_dict["x_0_linear_est_sys"])
        x_0_est = sympy.Matrix(vals_dict["x_0_linear_est_est"])
        output_names = [
            "system state",
            "estimated system state"

        ]
        time_steps = np.arange(start=0, stop=duration, step=dt)
        inputs = [sympy.Matrix([[0]]) for t in time_steps]
        run_name = "estimator-nonlinear"
        graph_location = f"resources/{run_name}.png"
        caption="Estimator in NonLinear performance"
        outputs = model_system(
            update=observer_update_wrapper,
            output=observer_output_wrapper,
            system_update=non_linear_update,
            system_output=linear_output,
            observer_update=observer_update,
            inputs=inputs,
            A=A, B=B, C=C, D=D, k=k, L=l, dt=dt, x_0=(x_0, x_0_est), f=total
        )
        true_outputs = []
        outputs = [[row[i] for row in outputs] for i in range(len(outputs[0]))]
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
