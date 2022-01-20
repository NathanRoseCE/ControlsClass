#! /usr/bin/env python

from LatexTemplater.TemplatePluginManager import load_plugins
from LatexTemplater.TemplateCore import TemplateCore
from glob import glob
from typing import List
from copy import deepcopy
import shutil
import os
import logging

load_plugins(["Filters"])

def generate(main_tex: str, texLoc: str, finalOut: str, varFiles: List[str]) -> None:
    theseVars = deepcopy(varFiles)
    inst = TemplateCore.instance()
    logging.info(f"generating pdf: {main_tex + '.pdf'}")
    inst.generate(main_tex, texLoc, varFiles=theseVars)
    finalName = extensionLessName(main_tex) + ".pdf"
    generated_pdf=os.path.join(texLoc, main_tex + ".pdf")
    final_pdf= os.path.join(finalOut, finalName)
    logging.info(f"Moving {generated_pdf} to {final_pdf}")
    shutil.move(generated_pdf, final_pdf)

def extensionLessName(fileName: str) -> str:
    return fileName.split("/")[-1].split(".")[0]
    
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    inst = TemplateCore.instance()
    inst.templateDir = "Templates"
    inst.resultsFolder = "TexFolder"
    varFiles=glob("data/*.json")
    generate("main", "TexFolder", "Output", varFiles=varFiles)
