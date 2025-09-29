import os
import sys
sys.path.insert(0, os.path.abspath('..'))   
sys.path.insert(0, os.path.abspath('../gui'))
sys.path.insert(0, os.path.abspath('../school'))


project = "School Management System (PyQt/tkinter)"
author = "Marc Abou Nader, Roy Baroudy"
copyright = "2025, Marc Abou Nader, Roy Baroudy"
release = "1.0.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
]

html_theme = "sphinx_rtd_theme"

autodoc_mock_imports = ["PyQt5"]
