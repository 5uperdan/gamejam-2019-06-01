from cx_Freeze import setup, Executable
import os
import sys

# may need something like these
#os.environ['TCL_LIBRARY'] = "C:\\Users\\danny\\Envs\\gamejam-2019-06-01\\tcl\\tcl8.6"
#os.environ['TK_LIBRARY'] = "C:\\Users\\danny\\Envs\\gamejam-2019-06-01\\tcl\\tk8.6"

os.environ['TCL_LIBRARY'] = sys.path[0] + "\\.win-buildrequirements\\tcl8.6"
os.environ['TK_LIBRARY'] = sys.path[0] + "\\.win-buildrequirements\\tk8.6"

setup(name="KNOCKING DOWN CAPITALISM",
      version="0.1",
      description="It's like robocop but with ninjas",
      options={"build_exe": {"packages": ["pygame", "pyglet"],
                             "include_files": ["assets"]}},
      executables=[Executable("main.py")])

# open terminal and run: python setup.py build
# or python setup.py bdist_msi to build an installation