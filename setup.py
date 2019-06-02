from cx_Freeze import setup, Executable
import os

#may need something like these
#os.environ['TCL_LIBRARY'] = "C:\\Program Files\\Python35\\tcl\\tcl8.6"
#os.environ['TK_LIBRARY'] = "C:\\Program Files\\Python35\\tcl\\tk8.6"


setup(name="KNOCKING DOWN CAPITALISM",
      version="0.1",
      description="It's like robocop but with ninjas",
      options={"build_exe": {"packages": ["pygame", "pyglet"],
                             "include_files": ["assets"]}},
      executables=[Executable("main.py")])

# open terminal and run: python setup.py build
# or python setup.py bdist_msi to build an installation