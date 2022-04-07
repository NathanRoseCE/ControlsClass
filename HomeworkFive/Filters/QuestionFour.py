from LatexTemplater.TemplateFilter import TemplateFilter
from typing import Iterable
from .snippets.model import ModelSystem, non_linear_update, linear_update, linear_output
import numpy as np
from LatexTemplater.TemplateCore import TemplateCore
import sympy
import matplotlib.pyplot as plt

def registrationInfo():
    return {
        QuestionFour.name: QuestionFour.filter
    }
    
class QuestionFour(TemplateFilter):
    name="question_four"

    @staticmethod
    def filter(run_info: str) -> str:
        duration = run_info["duration"]
        dt = run_info["dt"]
        x_0 = sympy.Matrix(run_info["x_0"])
        run_name = run_info["name"]
        caption = run_info["caption"] if "caption" in run_info else ""
        A = sympy.Matrix([
            [-2, 1],
            [0, -1]
        ])
        B = sympy.Matrix([
            [0],
            [1]
        ])
        C = sympy.eye(2)
        D = sympy.Matrix([[0],[0]])
        k = sympy.Matrix(run_info["k"])
        time_steps = [
            t for t in np.arange(start=0, stop=duration, step=dt)
        ]
        inputs = [
            sympy.Matrix([[0]]) for t in time_steps
        ]
        outputs = ModelSystem(
            update=non_linear_update,
            output=linear_output,
            x_0=x_0,
            inputs=inputs,
            k=k,
            dt=dt,
            C=C,
            D=D
        )
        graph_location = f"resources/{run_name}.png"
        QuestionFour.plotter(
            time_steps,
            outputs,
            graph_location,
            run_name,
        )
        inst = TemplateCore.instance()
        return inst.filter(
            "image",
            [f"../{graph_location}", caption, f"fig:{run_name}"]
        )                     

    @staticmethod
    def plotter(time_steps: Iterable[float],
                outputs: Iterable[sympy.Matrix],
                save_file: str,
                title_name: str,
                output_names: Iterable[str] = None):
        """
        takes the system outputs and plots them, returns the file path
        """
        fig = plt.figure()
        axis = fig.add_axes([0.15, 0.15, 0.75, 0.75])
        outputs = np.concatenate(outputs, axis=1)
        if output_names is None:
            output_names = []
            for i in range(len(outputs)):
                output_names.append(f"output {i}")

        for output, name in zip(outputs, output_names):
            axis.plot(time_steps, output.T, label=name)
            axis.set_title(title_name)
            axis.set_xlabel('Time(s)')
            axis.set_ylabel('System outputs')
            axis.legend()
            fig.savefig(save_file)
        
