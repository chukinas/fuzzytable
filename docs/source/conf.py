# Configuration file for the Sphinx documentation builder.
import os
import sys
# import sphinx_bootstrap_theme
# import sphinx_rtd_theme

#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------
# sys.path.insert(0, os.path.abspath('.'))
project_path = os.path.abspath('../..')
print('project path:', project_path)
sys.path.insert(0, project_path)


# -- Project information -----------------------------------------------------
project = 'fuzzytable'
copyright = '2019, Jonathan Chukinas'
author = 'Jonathan Chukinas'
release = '0.19'  # The full version, including alpha/beta/rc tags


# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'm2r',
    # 'sphinx_rtd_theme',
    'sphinx.ext.todo',
    'autodocsumm',  # pip install autodocsumm
]
autodoc_default_options = {
    'autosummary': True,
}
master_doc = 'index'
# https://github.com/readthedocs/readthedocs.org/issues/2569
# b/c RTD throws an error and the about page says this is the solution to it.

# Add any paths that contain templates here, relative to this directory.
templates_path = []  # ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# html_theme = 'sphinx_rtd_theme'
html_theme = 'alabaster'
html_theme_options = {
    'logo': 'logo.png',
    # 'logo': 'https://raw.githubusercontent.com/jonathanchukinas/fuzzytable/master/docs/source/images/logo.png',
    'github_user': 'jonathanchukinas',
    'github_repo': 'fuzzytable',
    'description': 'Read tables from messy spreadsheets'
}
# html_theme = 'bootstrap'
# html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
# https://github.com/readthedocs/readthedocs.org/issues/2569
# b/c RTD throws an error and the about page says this is the solution to it.


# -- Extension configuration -------------------------------------------------
# Napoleon settings
napoleon_google_docstring = True
# napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True

# TODOs
todo_include_todos = True
