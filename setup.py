import sys
from cx_Freeze import setup, Executable

packages = [
    'idna',
]
files = [
    'config',
    'assets'
]
excludes = ["tkinter"]
modules = []

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
      executables=[Executable("main.py", base=base, icon='assets/doc_icon.ico')])
