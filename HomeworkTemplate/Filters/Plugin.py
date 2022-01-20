from LatexTemplater.TemplateCore import TemplateCore
from . import Common


def initialize():
    """
    Registers all filters for templates
    """
    instance = TemplateCore.instance()
    registrationFuncs = [
        Common.registrationInfo
    ]
    for registerFunc in registrationFuncs:
        filterinfo = registerFunc()
        for name, filter in filterinfo.items():
            instance.registerFilter(name, filter)
