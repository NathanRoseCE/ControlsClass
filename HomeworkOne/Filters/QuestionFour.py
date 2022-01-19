from LatexTemplater.TemplateFilter import TemplateFilter
from LatexTemplater.TemplateCore import TemplateCore
from typing import Dict, Callable
import control

def registrationInfo() -> Dict[str, Callable[[any], str]]:
     return {
         StateSpace.name: StateSpace.filter,
         TransferFunction.name: TransferFunction.filter
     }
    
class StateSpace(TemplateFilter):
    name="FourSS"

    @staticmethod
    def filter(state: str) -> str:
        A = state["A"]
        B = state["B"]
        C = state["C"]
        D = state["D"]
        inst = TemplateCore.instance()
        return inst.filter("ss", (A,B,C,D))

class TransferFunction(TemplateFilter):
    name="FourTF"

    @staticmethod
    def filter(state: str) -> str:
        A = state["A"]
        B = state["B"]
        C = state["C"]
        D = state["D"]
        inst = TemplateCore.instance()
        
        return inst.filter("eq", inst.filter("tf", control.ss2tf(A,B,C,D)))
