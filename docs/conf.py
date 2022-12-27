# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os
import sys
sys.path.insert(0, os.path.abspath('../...'))
sys.setrecursionlimit(1500)
# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'sync'
copyright = '2022, Kapa Kudaibergenov'
author = 'Kapa Kudaibergenov'
release = '2022'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    # 'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    # 'sphinxcontrib.asciiart',
    'sphinx.ext.imgmath',
    'sphinx_rtd_theme',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Napoleon config
napoleon_custom_sections = [
    ('Optional arguments', 'params_style'),
    ('Variables', 'params_style'),
]

# More sphinx config
autoclass_content = 'both'

# Numfig
numfig = True

# Config of ASCII art
ascii_art_output_format = dict(html='.html', latex='.png', text='.txt')
