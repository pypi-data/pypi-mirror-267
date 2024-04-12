import os
import sys

project = "Armis Python Package"
copyright = "2024, Matthew Lange"
author = "Matthew Lange"

sys.path.insert(0, os.path.abspath("../../src"))
# sys.path.insert(0, os.path.abspath(".."))

import armis

release = armis.__version__.__version__
version = armis.__version__.__version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "numpydoc",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.ifconfig",
    "sphinx.ext.viewcode",
    "sphinx.ext.imgmath",
]


templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = "alabaster"
html_theme = "sphinx_material"

html_static_path = ["_static"]

html_theme_options = {
    "base_url": "http://github.com/mmlange/armis-python/",
    "repo_url": "http://github.com/mmlange/armis-python/",
    "repo_name": "Python package for Armis",
    "html_minify": True,
    "css_minify": True,
    "nav_title": "Python package for Armis",
    "logo_icon": "&#xe869",
    "globaltoc_depth": 2,
}
