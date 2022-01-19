from LatexTemplater.TemplateCore import TemplateCore
from . import Common
from . import QuestionOne
from . import QuestionFour


def initialize():
    """
    Registers all filters for templates
    """
    instance = TemplateCore.instance()
    registrationFuncs = [
        QuestionOne.registrationInfo,
        QuestionFour.registrationInfo,
        Common.registrationInfo
    ]
    for registerFunc in registrationFuncs:
        filterinfo = registerFunc()
        for name, filter in filterinfo.items():
            instance.registerFilter(name, filter)
