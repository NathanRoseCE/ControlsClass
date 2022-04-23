from LatexTemplater.TemplateFilter import TemplateFilter
from .snippets.equations_of_motion import *
from .snippets.feedback import *
from .snippets.model import *
from .snippets.responses import *
from .General import pre_process, plot
import numpy as np

def registrationInfo():
    return {
        ZeroInputResponse.name: ZeroInputResponse.filter,
        ZeroStateResponse.name: ZeroStateResponse.filter,
        TotalResponse.name: TotalResponse.filter
    }


class ZeroInputResponse(TemplateFilter):
    name="zero_input_response"

    @staticmethod
    def filter(vals_dict: str) -> str:
        A, B, x = linearized_update_equation(evaluate_vals=True, **vals_dict)
        C = sympy.Matrix([[1,1,1,1,1,1]])
        D = sympy.Matrix([[0]])
        if not vals_dict["enable_eat"]:
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
            run_name = "zero input"
            graph_location = f"resources/{run_name}.png"
            caption="Zero input Response"
            outputs = [model_system(
                update=linear_update,
                output=linear_output,
                inputs=inputs,
                A=A, B=B, C=C, D=D, dt=dt, x_0=x_0
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
        x_0 = sympy.Matrix(vals_dict["x_0s_linear"][0])
        no_input = zero_input_response(A, x_0)
        work = "the stm matrix can be calculated from A which is as follows\n"
        work += r"\begin{equation}"+"\n"
        work += r"\inverseLaplace{(sI-A)^{-1}}x_0"+"\n"
        work += r"\end{equation}"+"\n"
        work += r"which for an x_0 of $ x = "+latex_rounded(x_0)+"$\n"
        work += r"\begin{equation}"+"\n"
        work += latex_rounded(no_input)+"\n"
        work += r"\end{equation}"+"\n"
        return work

class ZeroStateResponse(TemplateFilter):
    name="zero_state_response"

    @staticmethod
    def filter(vals_dict: str) -> str:
        vals_dict = pre_process(vals_dict)
        A, B, x = linearized_update_equation(evaluate_vals=True, **vals_dict)
        C = sympy.Matrix([[1,1,1,1,1,1]])
        D = sympy.Matrix([[0]])
        if not vals_dict["enable_eat"]:
            duration = vals_dict["duration"]
            dt = vals_dict["dt"]
            x_0 = sympy.Matrix([[0],[0],[0],[0],[0],[0]])
            output_names = [
                f"u = {i}" for i in range(2)
            ]
            time_steps = np.arange(start=0, stop=duration, step=dt)
            inputs = [
                [sympy.Matrix([[i]]) for t in time_steps]
                for i in range(2)
            ]
            run_name = "zero_state"
            graph_location = f"resources/{run_name}.png"
            caption="zero state"
            outputs = [model_system(
                update=linear_update,
                output=linear_output,
                inputs=some_input,
                A=A, B=B, C=C, D=D, dt=dt, x_0=x_0
            ) for some_input in inputs]
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
        no_state = zero_state_response(A, B)
        work = "the stm matrix can be calculated from A which is as follows\n"
        work += r"\begin{equation}"+"\n"
        work += r"\inverseLaplace{(sI-A)^{-1}}x_0"+"\n"
        work += r"\end{equation}"+"\n"
        work += r"\begin{equation}"+"\n"
        work += latex_rounded(no_state)+"\n"
        work += r"\end{equation}"+"\n"
        return work

class TotalResponse(TemplateFilter):
    name = "total_response"

    @staticmethod
    def filter(vals_dict) -> str:
        vals_dict = pre_process(vals_dict)
        A, B, x = linearized_update_equation(evaluate_vals=True, **vals_dict)
        C = sympy.Matrix([[1,1,1,1,1,1]])
        D = sympy.Matrix([[0]])
        if not vals_dict["enable_eat"]:
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
            run_name = "full_response"
            graph_location = f"resources/{run_name}.png"
            caption="Full Response"
            outputs = [model_system(
                update=linear_update,
                output=linear_output,
                inputs=inputs,
                A=A, B=B, C=C, D=D, dt=dt, x_0=x_0
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
        x_0 = sympy.Matrix(vals_dict["x_0s_linear"][0])
        no_state = zero_state_response(A, B)
        no_input = zero_input_response(A, B)
        work = "the total response is:\n" 
        work += r"\begin{equation}"+"\n"
        work += "  x_{zs} + x_{zi}\n"
        work += r"\end{equation}"+"\n"
        work += r"\begin{equation}"+"\n"
        work += "  " + latex_rounded(no_state+no_input)+"\n"
        work += r"\end{equation}"+"\n"
        return work
