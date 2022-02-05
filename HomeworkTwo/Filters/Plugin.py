from LatexTemplater.TemplateCore import TemplateCore
from . import QuestionOne
from . import QuestionTwo
from . import QuestionThree
from . import Common


def initialize():
    """
    Registers all filters for templates
    """
    instance = TemplateCore.instance()
    registrationFuncs = [
        Common.registrationInfo,
        QuestionOne.registrationInfo,
        QuestionTwo.registrationInfo,
        QuestionThree.registrationInfo,
    ]
    for registerFunc in registrationFuncs:
        filterinfo = registerFunc()
        for name, filter in filterinfo.items():
            instance.registerFilter(name, filter)
