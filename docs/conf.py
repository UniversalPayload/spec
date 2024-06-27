# SPDX-License-Identifier: Apache-2.0
# -*- coding: utf-8 -*-
#
# UPL Specification documentation build configuration file
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
import time
import subprocess
# sys.path.insert(0, os.path.abspath('.'))

sys.path.append(os.path.abspath('extensions'))

# -- Project information -----------------------------------------------------

project = u'Universal Payload Specification'
copyright = u'2023, Universal Payload Workgroup'
author = u'Universal Payload Workgroup'

# The short X.Y version
try:
    version = str(subprocess.check_output(["git", "describe", "--dirty"]), 'utf-8').strip()
except:
    version = "unknown-rev"
# The full version, including alpha/beta/rc tags
# TEMP FIX: Hardcode the version here until Github resolves the Github Action Tag issue:
# https://github.com/orgs/community/discussions/62991
version = "v0.8"
release = version


# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
needs_sphinx = '7.3.7'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.githubpages',
    'sphinx.ext.todo',
    'sphinx.ext.graphviz'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The document name of the “master” document, that is,
# the document that contains the root toctree directive.
# Default is 'index', we set it here for supporting Sphinx<2.0
master_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'en'

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#today = ''
# Else, today_fmt is used as the format for a strftime call.
today_fmt = '%d %B %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# Include at the beginning of every source file that is read
with open('rst_prolog', 'rb') as pr:
    rst_prolog = pr.read().decode('utf-8')

rst_epilog = """
.. |SpecVersion| replace:: {versionnum}
""".format(
versionnum = version,
)

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

numfig = True

highlight_language = 'none'


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'furo'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {
    "source_repository": "https://github.com/universalpayload/spec/",
    "source_branch": "main",
    "source_directory": "docs/",
}

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
# Credit goes to 9elements Design Team for the great logo design :)
html_logo = "_images/upl-logo_round.png"

# The name of an image file (relative to this directory) to use as a favicon of
# the docs.  This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
html_favicon = "_images/upl-favicon.svg"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    'classoptions': ',oneside',
    'babel': '\\usepackage[english]{babel}',
    'sphinxsetup': 'hmargin=2cm',

    # The paper size ('letterpaper' or 'a4paper').
    #
    'papersize': 'a4paper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Latex figure (float) alignment
    #
    'figure_align': 'H',

    # Add or modify the preamble entry as follows:
    # Set \cftsecleader to remove auto numbering from Table of Content
    # set \setcounter{secnumdepth}{0} stop section numbering
    # Use makeatlatter to remove auto chapters & numbering from each section.
    # This is because the default latex "manual" format automatically
    # generates chapter and section numbering, overlapping the pre-configured
    # numberings, which will mess up the pdf.
    # Add 'longtable' support to prevent the table being truncated when it is
    # longer than one page during pdf generation.
    'preamble': r'''
\usepackage{tocloft}
\renewcommand{\cftsecleader}{\cftdotfill{\cftdotsep}}
\setcounter{secnumdepth}{0}
\makeatletter
\def\@makechapterhead#1{%
  \vspace*{50\p@}% Adjust the space above the chapter title as needed
  {\parindent \z@ \raggedright \normalfont
    \Huge\bfseries #1\par\nobreak
    \vskip 40\p@
  }}
\makeatother
\usepackage{longtable}
''',
}

# Release numbers with a qualifier (ex. '-rc', '-draft') get a watermark.
if '-' in release:
    latex_elements['preamble'] += '\\usepackage{draftwatermark}\\SetWatermarkScale{.45}\\SetWatermarkText{%s}' % (release)

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'upl-specification.tex', u'UPL Specification',
     u'github.com/universalpayload/spec', 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
latex_logo = "_images/upl-logo.png"

# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'upl-specification', u'UPL Specification',
     [author], 1)
]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'upl-specification', u'UPL Specification',
     author, 'UPLSpecification', 'Universal Payload specification.',
     'Miscellaneous'),
]


# -- Options for Epub output -------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = project

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#
# epub_identifier = ''

# A unique identification for the text.
#
# epub_uid = ''

# A list of files that should not be packed into the epub file.
epub_exclude_files = ['search.html']


# -- Extension configuration -------------------------------------------------

# -- Options for todo extension ----------------------------------------------

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False
