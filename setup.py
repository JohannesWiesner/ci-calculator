import sys
import os
from cx_Freeze import setup, Executable

build_exe_options = {

'includes': [
'numpy.core._methods','numpy.lib.format',
'matplotlib.backends.backend_tkagg','matplotlib.backends.backend_ps',
'matplotlib.backends.backend_pdf','matplotlib.backends.backend_pgf',
'matplotlib.backends.backend_ps','matplotlib.backends.backend_svg',
'scipy.sparse.csgraph._validation',
'scipy.spatial.ckdtree'
],

'excludes': [
'scipy.spatial.cKDTree' 
],

'include_files': [
'C:/Users/johwi/AppData/Local/Programs/Python/Python36-32/DLLs/tcl86t.dll',
'C:/Users/johwi/AppData/Local/Programs/Python/Python36-32/DLLs/tk86t.dll',
'C:/Users/johwi/Coding/ci-calculator/app_icon.ico'
],

'optimize': 2	
}

os.environ['TCL_LIBRARY'] = 'C:/Users/johwi/AppData/Local/Programs/Python/Python36-32/tcl/tcl8.6'
os.environ['TK_LIBRARY'] = 'C:/Users/johwi/AppData/Local/Programs/Python/Python36-32/tcl/tk8.6'

# GUI applications require a different base on Windows (the default is for a console application)
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(  name = "ci-calculator",
        version = "1.0.0",
        description = "A program for calculating and plotting confidence intervals used for psychodiagnostics",
        options={"build_exe": build_exe_options},
        executables = [Executable("C:/Users/johwi/Coding/ci-calculator/main.py", base=base)])