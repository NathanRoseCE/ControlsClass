from LatexTemplater.TemplateFilter import TemplateFilter
from LatexTemplater.TemplateCore import TemplateCore
from typing import Dict, Callable

def registrationInfo() -> Dict[str, Callable[[any], str]]:
     return {
         MFromSystem.name: MFromSystem.filter,
         K1FromSystem.name: K1FromSystem.filter,
         K3FromSystem.name: K3FromSystem.filter,
         CFromSystem.name: CFromSystem.filter,
         UFromSystem.name: UFromSystem.filter,
         NonLinearPosition.name: NonLinearPosition.filter,
         NonLinearVelocity.name: NonLinearVelocity.filter,
         LinearPosition.name: LinearPosition.filter,
         LinearVelocity.name: LinearVelocity.filter,
         StateSpace.name: StateSpace.filter
    }
    
class MFromSystem(TemplateFilter):
    name="MFromSystem"

    @staticmethod
    def filter(val: str) -> str:
        return str(val["m"])

class K1FromSystem(TemplateFilter):
    name="K1FromSystem"

    @staticmethod
    def filter(val: str) -> str:
        return str(val["k1"])

class K3FromSystem(TemplateFilter):
    name="K3FromSystem"

    @staticmethod
    def filter(val: str) -> str:
        return str(val["k3"])

class CFromSystem(TemplateFilter):
    name="CFromSystem"

    @staticmethod
    def filter(val: str) -> str:
        return str(val["c"])

class UFromSystem(TemplateFilter):
    name="UFromSystem"

    @staticmethod
    def filter(val: str) -> str:
        return str(val["u"])

class NonLinearPosition(TemplateFilter):
    name="OneNonLinearPosition"
    @staticmethod
    def filter(val: dict) -> str:
        system = val['system']
        return (r"w = \frac{" + f"{system['u']} + {system['k3']}w^3 - {system['c']}" +
                r"\dot w - " + f"{system['m']}" + r"\ddot w}{" + str(system["k1"]) + r"}")
    
class NonLinearVelocity(TemplateFilter):
    name="OneNonLinearVelocity"
    
    @staticmethod
    def filter(val: dict) -> str:
        system = val['system']
        return (r"\dot w = \frac{" + f"{system['u']} + {system['k3']}w^3 - {system['k1']}w" +
                f"- {system['m']}" + r"\ddot w}{" + str(system["c"]) + r"}")

def linearize(val: dict) -> dict:
    """
    linearizes the equation for question one given a set of values,
    returns state space equation of form
    w        =  | a_11  a_12 | + | b_1 |
    \dot w      | a_21  1_22 |   | b_2 |
    return dict is in the following format
    {
      "a": [[ a_11, a_12],
            [ a_21, a_22]],
      "b": [[b_1],[b_2]]
    }
    """
    return {
        "a": [[1,2],
              [3,4]],
        "b": [[5],
              [6]]
    }
    # raise NotImplimented
    
class LinearPosition(TemplateFilter):
    name="OneLinearPosition"

    @staticmethod
    def filter(val: dict) -> str:
        state = linearize(val)
        A = state["a"]
        B = state["b"]
        return f"w = {A[0][0]}w + {A[0][1]}\dot w + {B[0][0]}u"
        
    
class LinearVelocity(TemplateFilter):
    name="OneLinearVelocity"

    @staticmethod
    def filter(val: dict) -> str:
        state = linearize(val)
        A = state["a"]
        B = state["b"]
        return f"w = {A[1][0]}w + {A[1][1]}\dot w + {B[1][0]}u"


class StateSpace(TemplateFilter):
    name="OneStateSpace"

    @staticmethod
    def filter(val: dict) -> str:
        state = linearize(val)
        A = state["a"]
        B = state["b"]
        C = [[1,0],
             [0,1]]
        D = [[0],
             [0]]
        inst = TemplateCore.instance()
        return inst.filter("ss", (A,B,C,D))
