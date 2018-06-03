import sys
from cx_Freeze import setup, Executable

PYTHON_INSTALLATION = 'C:\\Users\\sungo\\Anaconda3'
files = ['config',
         'images',
         '{}\\Lib\\site-packages\\google_cloud_firestore-0.28.0.dist-info'.format(PYTHON_INSTALLATION),
         '{}\\Lib\\site-packages\\google_gax-0.15.16.dist-info'.format(PYTHON_INSTALLATION),
         '{}\\Lib\\site-packages\\google_api_core-0.1.4.dist-info'.format(PYTHON_INSTALLATION),
         '{}\\Lib\\site-packages\\google_cloud_core-0.28.1.dist-info'.format(PYTHON_INSTALLATION),
         '{}\\Lib\\site-packages\\grpcio-1.12.0.dist-info'.format(PYTHON_INSTALLATION)]
packages = ["os",
            "spacy.lang.en",
            "pkg_resources._vendor",
            "idna",
            "google",
            "google.auth"]
excludes = ["tkinter"]
modules = ["numpy.core._methods",
           "numpy.lib.format",
           "cymem",
           "murmurhash",
           "lxml._elementpath",
           "cytoolz._signatures",
           "thinc.neural._classes.difference",
           "spacy.tokens.underscore",
           "spacy.tokens.printers"]

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
      executables=[Executable("main.py", base=base, icon='doc_icon.ico')])
