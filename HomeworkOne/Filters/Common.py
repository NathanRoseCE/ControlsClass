from LatexTemplater.TemplateFilter import TemplateFilter
from LatexTemplater.TemplateCore import TemplateCore
from typing import Dict, Callable, Tuple, Iterable

def registrationInfo() -> Dict[str, Callable[[any], str]]:
     return {
         TODO.name: TODO.filter,
         StateSpace.name: StateSpace.filter
    }
    
class TODO(TemplateFilter):
    name="TODO"

    @staticmethod
    def filter(val: str) -> str:
        return r"{\LARGE \color{red} TODO: " + val + r"}"

class StateSpace(TemplateFilter):
    name="StateSpace"

    @staticmethod
    def filter(system: Tuple[Iterable[Iterable[any]]]) -> str:
        inst = TemplateCore.instance()
        A, B, C, D = system
        equation_one = inst.filter(
            "eq", (r"\dot x = " +
                         inst.filter("bmatrix", A) +  "x + " + 
                         inst.filter("bmatrix", B) +  "u")
        )
        equation_two = inst.filter(
            "eq", (r"y = " +
                         inst.filter("bmatrix", C) +  "x + " + 
                         inst.filter("bmatrix", D) +  "u")
        )
        return equation_one + equation_two

