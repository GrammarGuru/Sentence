import sys
from cx_Freeze import setup, Executable

files = ['newspapers.json', 
         'style.json']
packages = ["os", 
            "spacy.lang.en", 
            "pkg_resources._vendor",
            "idna",
            "google",
            "google.cloud"]

excludes = ["tkinter"]
modules = ["numpy.core._methods", 
           "numpy.lib.format", 
           "cymem", 
           "murmurhash",
           "lxml._elementpath",
           "cytoolz._signatures",
           "thinc.neural._classes.difference"]

build_exe_options = {"packages": packages,
                     "excludes": excludes,
                     "includes": modules,
                     "include_files": files}


# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(name="Sentence",
      version="0.1",
      description="Sentence Worksheet Maker",
      options={"build_exe": build_exe_options},
      executables=[Executable("main.py", base=base)])
