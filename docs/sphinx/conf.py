#
# This file is part of BDC-Catalog.
# Copyright (C) 2019-2020 INPE.
#
# BDC-Catalog is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#

"""Configuration file for the BDC-Catalog extension's documentation.

The documentation system is based on Sphinx. If you want to know
more about the options to be used for configuration, please, see:
- https://www.sphinx-doc.org/en/master/usage/configuration.html
"""

import bdc_catalog
import sphinx_rtd_theme

# -- Project information -----------------------------------------------------

project = 'BDC-Catalog'
copyright = '2019-2020, INPE'
author = 'Brazil Data Cube Team'
release = bdc_catalog.__version__

# -- General configuration ---------------------------------------------------

# Enabled Sphinx extensions.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.napoleon',
    'sphinx.ext.todo',
    'sphinx_copybutton',
    'sphinx_rtd_theme',
    # 'sphinx_tabs.tabs',
]

# Paths that contain templates, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store'
]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.
html_theme = 'sphinx_rtd_theme'

html_theme_options = {
    'html_baseurl': 'https://brazil-data-cube.github.io/',
    'analytics_id': 'XXXXXXXXXX',
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'both',
    'style_external_links': True,
    'github_url': 'https://github.com/brazil-data-cube/bdc-catalog',
    'style_nav_header_background': '#2980B9',
    'collapse_navigation': True,
    'sticky_navigation': False,
    'navigation_depth': 3,
    'includehidden': True,
    'titles_only': False
}

# html_theme_path = ''

# html_style = ''

html_title = 'BDC-Catalog'

html_baseurl = 'https://brazil-data-cube.github.io/'

html_context = {
    'display_github': False,
    'github_user': 'brazil-data-cube',
    'github_repo': 'bdc-db',
    'last_updated': False,
    # 'commit': False,
}

html_show_sourcelink = False

html_logo = './img/logo-bdc.png'

html_favicon = './img/favicon.ico'

# html_static_path = ['_static']

html_css_files = [ ]

html_last_updated_fmt = '%b %d, %Y'

html_show_sphinx = False

html_search_language = 'en'

numfig = True

numfig_format = {
    'figure': 'Figure %s -',
    'table': 'Table %s -',
    'code-block': 'Code snippet %s -',
    'section': 'Section %s.'
}

# def setup(app):
#     app.add_stylesheet('bdc-db.css')


# todo_include_todos = True
# todo_emit_warnings = True
master_doc = 'index'
