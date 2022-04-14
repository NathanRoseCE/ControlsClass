from LatexTemplater.TemplateCore import TemplateCore
from . import Common
from . import Introduction
from . import ControllerDesign
from . import ObserverDesign


def initialize():
    """
    Registers all filters for templates
    """
    instance = TemplateCore.instance()
    registrationFuncs = [
        Common.registrationInfo,
        Introduction.registrationInfo,
        ControllerDesign.registrationInfo,
        ObserverDesign.registrationInfo
    ]
    for registerFunc in registrationFuncs:
        filterinfo = registerFunc()
        for name, filter in filterinfo.items():
            instance.registerFilter(name, filter)
