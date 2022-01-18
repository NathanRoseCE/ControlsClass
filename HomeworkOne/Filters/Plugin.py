from LatexTemplater.TemplateCore import TemplateCore
from . import QuestionOne
from . import Common


def initialize():
    """
    Registers all filters for templates
    """
    instance = TemplateCore.instance()
    registrationFuncs = [
        QuestionOne.registrationInfo,
        Common.registrationInfo
    ]
    for registerFunc in registrationFuncs:
        filterinfo = registerFunc()
        for name, filter in filterinfo.items():
            instance.registerFilter(name, filter)