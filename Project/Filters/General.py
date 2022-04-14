import sympy
import matplotlib.pyplot as plt
from typing import Iterable

def pre_process(config):
    # config["desired_controller_eigenvalues"] = tuple(
    #     config["desired_controller_eigenvalues"]
    # )
    # config["x_0s"] = tuple([
    #     tuple([tuple(val) for val in x_0]) for x_0 in config["x_0s"]
    # ])
    return config
    

ROUND_TO=3
def latex_rounded(expr):
    return sympy.latex(expr.xreplace({n : round(n, ROUND_TO) for n in expr.atoms(sympy.Number)}))

def parse_eigenvalues(vals):
    eigs = []
    for val in vals:
        if not "imaginary" in val:
            eigs.append(
                val["real"]
            )
        else:
            eigs.append(
                val["real"] +
                (val["imaginary"]*1j)
            )
            eigs.append(
                val["real"] - 
                (val["imaginary"]*1j)
            )
        
    return eigs



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
