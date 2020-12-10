# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('../SmartPlanner'))
autodoc_mock_imports = ["django","bs4", "SmartPlanner", "manage"] # эта строчка убирает модули
# autoclass_content = ['both']

# Loads of configuration settings

# # This is the expected signature of the handler for this event, cf doc
# def autodoc_skip_member_handler(app, what, name, obj, skip, options):
#     # Basic approach; you might want a regex instead
#     return name.startswith("forms")

# # Automatically called by sphinx at startup
# def setup(app):
#     # Connect the autodoc-skip-member event from apidoc to the callback
#     app.connect('autodoc-skip-member', autodoc_skip_member_handler)


# -- Project information -----------------------------------------------------

project = 'SmartPlanner'
copyright = '2020, Gleb Sorokin, Olga Toporkova'
author = 'Gleb Sorokin, Olga Toporkova'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']