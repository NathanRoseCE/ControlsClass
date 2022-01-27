from LatexTemplater.TemplateFilter import TemplateFilter
from LatexTemplater.TemplateCore import TemplateCore
from typing import Dict, Callable, Tuple, Iterable, Any
from control import tf
import control
import numpy as np

def registrationInfo() -> Dict[str, Callable[[Any], str]]:
     return {
          TODO.name: TODO.filter,
          StateSpace.name: StateSpace.filter,
          Equation.name: Equation.filter,
          InlineEquation.name: InlineEquation.filter,
          TransferFunction.name: TransferFunction.filter,
          Fraction.name: Fraction.filter,
          Polynomial.name: Polynomial.filter,
          Float.name: Float.filter,
          TFObj.name: TFObj.filter,
          Zeros.name: Zeros.filter,
          Poles.name: Poles.filter,
          CSV.name: CSV.filter,
          ComplexCSV.name: ComplexCSV.filter,
          Imaginary.name: Imaginary.filter,
          ImaginaryConjugate.name: ImaginaryConjugate.filter
    }
    
class TODO(TemplateFilter):
    name="TODO"

    @staticmethod
    def filter(val: str) -> str:
        return r"{\LARGE \color{red} TODO: " + val + r"}"

class Equation(TemplateFilter):
     name="eq"

     @staticmethod
     def filter(val:str) -> str:
          return (r"\begin{equation}"  + "\n" + 
                  val.strip() +
                  r"\end{equation}"  + "\n")

class InlineEquation(TemplateFilter):
     name="inline"

     @staticmethod
     def filter(val:str) -> str:
          return f"${val.strip()}$"
     
class StateSpace(TemplateFilter):
    name="ss"

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


class TransferFunction(TemplateFilter):
    name="tf"

    @staticmethod
    def filter(transfer: tf) -> str:
         """
         Takes a 2d list of values representing the coefficients in the numerator and denominator
         """
         inst = TemplateCore.instance()
         scipyLTI = transfer.returnScipySignalLTI()
         lti_response = []
         for output in scipyLTI:
              out_responses = []
              for input in output:
                   out_responses.append(
                        inst.filter("frac", {
                             "var": "s",
                             "numerator": input.num,
                             "denominator": input.den
                        })
                   )
              lti_response.append(out_responses)
         return inst.filter("bmatrix", lti_response)

class TFObj(TemplateFilter):
     name="tfObj"

     @staticmethod
     def filter(vals: dict) -> str:
          numerator = vals["numerator"]
          denominator = vals["denominator"]
          return control.TransferFunction(numerator, denominator)

class Zeros(TemplateFilter):
     name="zeros"

     @staticmethod
     def filter(linearSys) -> Iterable[complex]:
          return control.zero(linearSys)

class Poles(TemplateFilter):
     name="poles"

     @staticmethod
     def filter(linearSys) -> Iterable[complex]:
          return control.pole(linearSys)

class CSV(TemplateFilter):
     name="csv"

     @staticmethod
     def filter(vals: Iterable[any]) -> str:
          return ", ".join([str(val) for val in vals])

class ComplexCSV(TemplateFilter):
     name="complexCsv"

     @staticmethod
     def filter(vals: Iterable[complex]) -> str:
          inst = TemplateCore.instance()
          return inst.filter(
               "csv",
               [inst.filter("imag_conj", val) for val in ComplexCSV.combineConjugates(vals)]
          )

     @staticmethod
     def combineConjugates(vals: Iterable[complex]) -> str:
          """
          returns only the conjugates with a positive i
          """
          conjugates = []
          for val in vals:
               if np.iscomplexobj(val):
                    val = val.real + (abs(val.imag)*1j)
                    if val in conjugates:
                         continue
               conjugates.append(val)
          return conjugates
          

class Fraction(TemplateFilter):
     name="frac"

     @staticmethod
     def filter(vals: dict) -> str:
          var= vals["var"]
          numerator = vals["numerator"]
          denominator = vals["denominator"]
          inst = TemplateCore.instance()
          frac_str = r"\frac{"
          frac_str += inst.filter("poly", {
               "var": var,
               "coeffs": numerator
          })
          frac_str += r"}{"
          frac_str += inst.filter("poly", {
               "var": var,
               "coeffs": denominator
          })
          frac_str += r"}"
          return frac_str

class Polynomial(TemplateFilter):
     name="poly"

     @staticmethod
     def filter(vals:dict) -> str:
          inst = TemplateCore.instance()
          var = vals["var"]
          coefficents = vals["coeffs"]
          poly_str = ""
          for i, num in enumerate(coefficents):
               rounded = float(
                    inst.filter("float", num)
               )
               if rounded != 0:
                    sign = ""
                    if not i == 0:
                         sign = (" + " if rounded > 0 else " - ")
                    poly_str += sign + str(abs(rounded))
                    exponent = len(coefficents)-i-1
                    if not exponent == 0:
                         poly_str += "s"
                         if not exponent == 1:
                              poly_str += r"^{" + str(exponent) + r"}"
          return poly_str

class Float(TemplateFilter):
     name="float"
     ROUND_TO = 3
     def filter(val: float) -> str:
          """
          rounds the float to ROUND_TO decimal places and casts to a string
          """
          return str(round(val, Float.ROUND_TO))

class Imaginary(TemplateFilter):
     name="imag"

     @staticmethod
     def filter(val: complex) -> str:
          """
          rounds an imaginary number to ROUND_TO decimal places and
          casts to a string
          """
          inst = TemplateCore.instance()
          real_str = ""
          imag_str = ""
          if val.real != 0:
               real_str += inst.filter("float", val.real)
          if val.imag != 0:
               if val.imag > 0:
                    imag_str += "+"
               else:
                    imag_str += "-"
               imag_str += inst.filter("float", val.imag)
          if val.real == 0 and val.imag == 0:
               return "0"
          elif val.real != 0 and val.imag == 0:
               return real_str
          elif val.real == 0 and val.imag != 0:
               return imag_str
          else:
               return real_str + imag_str

class ImaginaryConjugate(TemplateFilter):
     name="imag_conj"

     @staticmethod     
     def filter(val: complex, conj: bool=False) -> str:
          """
          rounds an imaginary number to ROUND_TO decimal places and
          casts to a string
          This one will do \pm instead of a normal + or - i
          """
          inst = TemplateCore.instance()
          real_str = ""
          imag_str = ""
          if val.real != 0:
               real_str += inst.filter("float", val.real)
          if val.imag != 0:
               imag_str += r" \pm " + inst.filter("float", val.imag) + "j"
          if val.real == 0 and val.imag == 0:
               return "0"
          elif val.real != 0 and val.imag == 0:
               return real_str
          elif val.real == 0 and val.imag != 0:
               return imag_str
          else:
               return real_str + imag_str
