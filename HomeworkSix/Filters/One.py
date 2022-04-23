from LatexTemplater.TemplateCore import TemplateCore
from LatexTemplater.TemplateFilter import TemplateFilter
from .snippets.observer_design import *
from .snippets.model import *
import numpy as np
import matplotlib.pyplot as plt

def plot(time_steps: Iterable[float],
         outputs: Iterable[Iterable[sympy.Matrix]],
         save_file: str,
         title_name: str,
         output_names: Iterable[str] = None):
    """
    takes the system outputs and plots them, returns the file path
    """
    fig = plt.figure()
    axis = fig.add_axes([0.15, 0.15, 0.75, 0.75])
    if output_names is None:
        output_names = []
        for i in range(len(outputs)):
            output_names.append(f"output {i}")

    for output, name in zip(outputs, output_names):
        axis.plot(time_steps, [val[0,0] for val in output], label=name)
    axis.set_title(title_name)
    axis.set_xlabel('Time(s)')
    axis.set_ylabel('System outputs')
    axis.legend()
    fig.savefig(save_file)

def registrationInfo():
    return {
        LDesign.name: LDesign.filter,
        LModel.name: LModel.filter
    }

          
class LDesign(TemplateFilter):
    name="design_l"

    @staticmethod
    def filter(vals_dict: str) -> str:
        A = sympy.Matrix(vals_dict["A"])
        B = sympy.Matrix(vals_dict["B"])
        C = sympy.Matrix(vals_dict["C"])
        D = sympy.Matrix(vals_dict["D"])
        eigs = vals_dict["desired_eigenvalues"]
        l, work = generate_l(A=A,
                             B=B,
                             multi_C=C,
                             desired_eigenvalues=eigs)
        return work

class LModel(TemplateFilter):
    name="model_l"

    def filter(vals_dict: any) -> str:
        A = sympy.Matrix(vals_dict["A"])
        B = sympy.Matrix(vals_dict["B"])
        C = sympy.Matrix(vals_dict["C"])
        D = sympy.Matrix(vals_dict["D"])
        k = sympy.Matrix(vals_dict["K"])
        eigs = vals_dict["desired_eigenvalues"]
        l, work = generate_l(A=A,
                             B=B,
                             multi_C=C,
                             desired_eigenvalues=eigs)
        duration = vals_dict["duration"]
        dt = vals_dict["dt"]
        x_0 = sympy.Matrix(vals_dict["x_0_sys"])
        x_0_est = sympy.Matrix(vals_dict["x_0_est"])
        output_names = [
            "system state",
            "estimated system state"
        ]
        time_steps = np.arange(start=0, stop=duration, step=dt)
        inputs = [sympy.Matrix([[0],[0]]) for t in time_steps]
        run_name = "estimator-linear"
        graph_location = f"resources/{run_name}.png"
        caption="Estimator in NonLinear performance"
        outputs = model_system(
            update=observer_update_wrapper,
            output=observer_output_wrapper,
            system_update=linear_update,
            system_output=linear_output,
            observer_update=observer_update,
            inputs=inputs,
            A=A, B=B, C=C, D=D, k=k, L=l, dt=dt, x_0=(x_0, x_0_est)
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
