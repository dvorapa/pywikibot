"""Configuration file for Sphinx."""
#
# (C) Pywikibot team, 2014-2024
#
# Distributed under the terms of the MIT license.
#
# Pywikibot documentation build configuration file, created by
# sphinx-quickstart on Sun Jun 26 00:00:43 2016.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.
from __future__ import annotations

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use Path.resolve() to make it absolute, like shown here.
#
import os
import re
import sys
import warnings
from pathlib import Path


try:
    import tomllib
except ImportError:
    import tomli as tomllib


# Deprecated classes will generate warnings as Sphinx processes them.
# Ignoring them.

warnings.simplefilter(action='ignore', category=FutureWarning)

repo_dir = Path(__file__).resolve().parents[1]
sys.path = [str(repo_dir), str(repo_dir / 'pywikibot')] + sys.path

os.environ['PYWIKIBOT_NO_USER_CONFIG'] = '1'
import pywikibot  # noqa: E402


# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
needs_sphinx = '8.0.2'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'notfound.extension',
    'sphinx_copybutton',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosectionlabel',
    'sphinx.ext.autosummary',
    'sphinx.ext.extlinks',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinxext.opengraph',
]


# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a dict:
#
# source_suffix = {'.rst': 'restructuredtext'}

# The encoding of source files.
#
# source_encoding = 'utf-8-sig'

# The master toctree document.
root_doc = 'index'

# General information about the project.
filepath = Path().absolute().parent / 'pyproject.toml'
with open(filepath, 'rb') as f:
    meta_data = tomllib.load(f)

project = meta_data['project']['name'].title()
project_copyright = pywikibot.__copyright__  # alias since Python 3.5
author = meta_data['project']['maintainers'][0]['name']

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = pywikibot.__version__.partition('.dev')[0]
# The full version, including alpha/beta/rc tags.
release = pywikibot.__version__

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'en'

# There are two options for replacing |today|: either, you set today to some
# non-false value, then it is used:
#
# today = ''
#
# Else, today_fmt is used as the format for a strftime call.
#
# today_fmt = '%B %d, %Y'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# These patterns also affect html_static_path and html_extra_path
exclude_patterns = ['_build']

# The reST default role (used for this markup: `text`) to use for all
# documents.
#
default_role = 'py:obj'

# If true, '()' will be appended to :func: etc. cross-reference text.
#
# add_function_parentheses = True

# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
#
# add_module_names = True

# If true, sectionauthor and moduleauthor directives will be shown in the
# output. They are ignored by default.
#
# show_authors = False

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'default'


# A list of ignored prefixes for module index sorting.
# modindex_common_prefix = []

# If true, keep warnings as "system message" paragraphs in the built documents.
# keep_warnings = False

# If true, `todo` and `todoList` produce output, else they produce nothing.
# todo_include_todos = False


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'furo'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#


# Add any paths that contain custom themes here, relative to this directory.
# html_theme_path = []

# The name for this set of Sphinx documents.
# "<project> v<release> documentation" by default.
#
# html_title = 'test vtest'

# A shorter title for the navigation bar.  Default is the same as html_title.
#
# html_short_title = None

# The name of an image file (relative to this directory) to place at the top
# of the sidebar.
#
html_logo = '_static/Pywikibot_MW_gear_icon.svg'

# Use a PNG version of the logo in OpenGraph social cards
# (needed because SVG is not supported)

ogp_social_cards = {
    'image': '_static/Pywikibot_MW_gear_icon.png',
}

# The name of an image file (relative to this directory) to use as a favicon of
# the docs. This file should be a Windows icon file (.ico) being 16x16 or 32x32
# pixels large.
#
html_favicon = '_static/Pywikibot.ico'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Add any extra paths that contain custom files (such as robots.txt or
# .htaccess) here, relative to this directory. These files are copied
# directly to the root of the documentation.
#
# html_extra_path = []

# If not None, a 'Last updated on:' timestamp is inserted at every page
# bottom, using the given strftime format.
# The empty string is equivalent to '%b %d, %Y'.
#
# html_last_updated_fmt = None

# Custom sidebar templates, maps document names to template names.
#
# html_sidebars = {}

# Additional templates that should be rendered to pages, maps page names to
# template names.
#
# html_additional_pages = {}

# If false, no module index is generated.
#
# html_domain_indices = True

# If false, no index is generated.
#
# html_use_index = True

# If true, the index is split into individual pages for each letter.
#
html_split_index = True

docs_url = 'https://gerrit.wikimedia.org/g/pywikibot/core/%2B/HEAD/docs/'

# HTML Theme Colors
# changed to match the palette as described on
# https://meta.wikimedia.org/wiki/Brand/colours

color_primary_blue = '#0C57A8'
color_blue_bg_light = '#0C57A81B'
color_blue_bg_dark = '#0C57A822'

color_blue_text_dark = '#94D5FF'

color_primary_red = '#990000'
color_red_bg_light = '#99000011'
color_red_bg_dark = '#99000014'

color_red_text_dark = '#FF5151'

color_primary_green = '#339966'
color_green_bg_light = '#33996612'
color_green_bg_dark = '#33996633'

color_yellow = '#F0BC00'
color_yellow_bg = '#F0BC0022'

color_brightblue = '#049DFF'
color_brightblue_bg = '#049DFF22'

color_purple = '#5748B5'
color_purple_bg = '#5748B52A'

html_theme_options = {
    'source_edit_link': docs_url + '{filename}',
    'navigation_with_keys': True,
    'light_css_variables': {
        'color-brand-primary': color_primary_blue,
        'color-link': color_primary_blue,
        'color-link--hover': color_primary_blue,
        'color-problematic': color_primary_red,
        'color-admonition-title--note': color_primary_blue,
        'color-admonition-title-background--note': color_blue_bg_light,
        'color-admonition-title--seealso': color_primary_blue,
        'color-admonition-title-background--seealso': color_blue_bg_light,
        'color-admonition-title--caution': color_yellow,
        'color-admonition-title-background--caution': color_yellow_bg,
        'color-admonition-title--warning': color_yellow,
        'color-admonition-title-background--warning': color_yellow_bg,
        'color-admonition-title--danger': color_primary_red,
        'color-admonition-title-background--danger': color_red_bg_light,
        'color-admonition-title--error': color_primary_red,
        'color-admonition-title-background--error': color_red_bg_light,
        'color-admonition-title--attention': color_primary_red,
        'color-admonition-title-background--attention': color_red_bg_light,
        'color-admonition-title--hint': color_primary_green,
        'color-admonition-title-background--hint': color_green_bg_light,
        'color-admonition-title--tip': color_primary_green,
        'color-admonition-title-background--tip': color_green_bg_light,
        'color-admonition-title--important': color_brightblue,
        'color-admonition-title-background--important': color_brightblue_bg,
        'color-admonition-title': color_purple,
        'color-admonition-title-background': color_purple_bg,
    },
    'dark_css_variables': {
        'color-brand-primary': color_blue_text_dark,
        'color-link': color_blue_text_dark,
        'color-link--hover': color_blue_text_dark,
        'color-problematic': color_red_text_dark,
        'color-admonition-title--note': color_primary_blue,
        'color-admonition-title-background--note': color_blue_bg_dark,
        'color-admonition-title--seealso': color_primary_blue,
        'color-admonition-title-background--seealso': color_blue_bg_dark,
        'color-admonition-title--caution': color_yellow,
        'color-admonition-title-background--caution': color_yellow_bg,
        'color-admonition-title--warning': color_yellow,
        'color-admonition-title-background--warning': color_yellow_bg,
        'color-admonition-title--danger': color_primary_red,
        'color-admonition-title-background--danger': color_red_bg_dark,
        'color-admonition-title--error': color_primary_red,
        'color-admonition-title-background--error': color_red_bg_dark,
        'color-admonition-title--attention': color_primary_red,
        'color-admonition-title-background--attention': color_red_bg_dark,
        'color-admonition-title--hint': color_primary_green,
        'color-admonition-title-background--hint': color_green_bg_dark,
        'color-admonition-title--tip': color_primary_green,
        'color-admonition-title-background--tip': color_green_bg_dark,
        'color-admonition-title--important': color_brightblue,
        'color-admonition-title-background--important': color_brightblue_bg,
        'color-admonition-title': color_purple,
        'color-admonition-title-background': color_purple_bg,
    }
}

# If true, links to the reST sources are added to the pages.
#
# html_show_sourcelink = True

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
#
# html_show_sphinx = True

# If true, "(C) Copyright ..." is shown in the HTML footer. Default is True.
#
# html_show_copyright = True

# If true, an OpenSearch description file will be output, and all pages will
# contain a <link> tag referring to it.  The value of this option must be the
# base URL from which the finished HTML is served.
#
# html_use_opensearch = ''

# This is the file name suffix for HTML files (e.g. ".xhtml").
# html_file_suffix = None

# Language to be used for generating the HTML full-text search index.
# Sphinx supports the following languages:
#   'da', 'de', 'en', 'es', 'fi', 'fr', 'hu', 'it', 'ja'
#   'nl', 'no', 'pt', 'ro', 'ru', 'sv', 'tr', 'zh'
#
# html_search_language = 'en'

# A dictionary with options for the search language support, empty by default.
# 'ja' uses this config value.
# 'zh' user can custom change `jieba` dictionary path.
#
# html_search_options = {'type': 'default'}

# The name of a javascript file (relative to the configuration directory) that
# implements a search results scorer. If empty, the default will be used.
#
# html_search_scorer = 'scorer.js'

# Output file base name for HTML help builder.
htmlhelp_basename = project + release.replace('.', '')

# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (root_doc, 'Pywikibot.tex', 'Pywikibot Documentation',
     author, 'manual'),
]

# The name of an image file (relative to this directory) to place at the top of
# the title page.
#
# latex_logo = None

# If true, show page references after internal links.
#
# latex_show_pagerefs = False

# If true, show URL addresses after external links.
#
# latex_show_urls = False

# Documents to append as an appendix to all manuals.
#
# latex_appendices = []

# If false, no module index is generated.
#
# latex_domain_indices = True


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (root_doc, project, 'Pywikibot Documentation',
     [author], 1)
]

manpages_url = 'https://www.mediawiki.org/wiki/Manual:Pywikibot/{path}'
# If true, show URL addresses after external links.
#
# man_show_urls = False


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (root_doc, project, 'Pywikibot Documentation',
     author, project, 'One line description of project.',
     'Miscellaneous'),
]

# Documents to append as an appendix to all manuals.
#
# texinfo_appendices = []

# If false, no module index is generated.
#
# texinfo_domain_indices = True

# How to display URL addresses: 'footnote', 'no', or 'inline'.
#
# texinfo_show_urls = 'footnote'

# If true, do not generate a @detailmenu in the "Top" node's menu.
#
# texinfo_no_detailmenu = False

# If false, do not generate in manual @ref nodes.
#
# texinfo_cross_references = False

numfig = True

# Other settings
show_authors = True
todo_include_todos = True
autodoc_typehints = 'description'
# autosectionlabel_prefix_document = True
suppress_warnings = ['autosectionlabel.*']
toc_object_entries_show_parents = 'hide'

# Napoleon settings
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_custom_sections = ['Advice', 'Advices', 'Hints', 'Rights', 'Tips']

python_use_unqualified_type_names = True
modindex_common_prefix = ['pywikibot.scripts.']

# Pywikibot theme style
html_permalinks_icon = '#'
html_css_files = [
    'css/pywikibot.css',
]


extlinks = {
    # MediaWiki API
    'api': ('https://www.mediawiki.org/wiki/API:%s', 'API:%s'),
    # Python bug tracker
    'issue': ('https://github.com/python/cpython/issues/%s',
              'Python issue %s'),
    # Phabricator tasks
    'phab': ('https://phabricator.wikimedia.org/%s', '%s'),
    # Python howto link
    'pyhow': ('https://docs.python.org/3/howto/%s', 'Python Howto %s'),
    # Python library link
    'pylib': ('https://docs.python.org/3/library/%s', 'Python Library %s'),
    # Generic Python link; should be used with explicit title
    'python': ('https://docs.python.org/3/%s', None),
    # Pywikibot source (on Phabricator)
    'source': (
        'https://phabricator.wikimedia.org/diffusion/PWBC/browse/master/%s.py',
        '%s'),
    'wiki': ('https://en.wikipedia.org/wiki/%s', '%s')
}


def pywikibot_docstring_fixups(app, what, name, obj, options, lines):
    """Remove plain 'Initializer.' or 'Allocator.' docstring.

    .. versionchanged:: 8.2
       remove 'Allocator.' docstring too.
    """
    if what not in ('class', 'exception'):
        return

    if lines and lines[0] in ('Initializer.', 'Allocator.'):
        lines[:] = lines[2:]


def pywikibot_script_docstring_fixups(app, what, name, obj, options, lines):
    """Pywikibot specific conversions."""
    from scripts.cosmetic_changes import warning

    if what != 'module':
        return

    if not name.startswith('scripts.'):
        return

    length = 0
    for index, line in enumerate(lines):
        # highlight the first line
        if index == 0:  # highlight the first line
            lines[0] = f"**{line.strip('.')}**"

        # add link for pagegenerators options
        elif line == '&params;':
            lines[index] = ('This script supports use of '
                            ':py:mod:`pagegenerators` arguments.')

        # add link for fixes
        elif name == 'scripts.replace' and line == '&fixes-help;':
            lines[index] = ('                  The available fixes are listed '
                            'in :py:mod:`pywikibot.fixes`.')

        # replace cosmetic changes warning
        elif name == 'scripts.cosmetic_changes' and line == '&warning;':
            lines[index] = warning

        # Initiate code block except pagegenerator arguments follows
        elif (line.endswith(':') and not line.lstrip().startswith(':')
                and 'Traceback (most recent call last)' not in line):
            for afterline in lines[index + 1:]:
                if not afterline:
                    continue
                if afterline != '&params;':
                    lines[index] = line + ':'
                break

        # adjust options
        if line.startswith('-'):
            # Indent options
            match = re.match(r'-[^ ]+? +', line)
            if match:
                length = len(match[0])
            lines[index] = ' ' + line
        elif length and line.startswith(' ' * length):
            # Indent descriptions of options (as options are indented)
            lines[index] = ' ' + line
        elif line:
            # Reset length
            length = 0


def pywikibot_family_classproperty_getattr(obj, name, *defargs):
    """Custom getattr() to get classproperty instances."""
    from sphinx.util.inspect import safe_getattr

    from pywikibot.family import Family
    from pywikibot.tools import classproperty

    if not isinstance(obj, type) or not issubclass(obj, Family):
        return safe_getattr(obj, name, *defargs)

    for base_class in obj.__mro__:
        try:
            prop = base_class.__dict__[name]
        except KeyError:
            continue

        if not isinstance(prop, classproperty):
            return safe_getattr(obj, name, *defargs)

        return prop

    return safe_getattr(obj, name, *defargs)


def setup(app):
    """Implicit Sphinx extension hook."""
    app.connect('autodoc-process-docstring', pywikibot_docstring_fixups)
    app.connect('autodoc-process-docstring', pywikibot_script_docstring_fixups)
    app.add_autodoc_attrgetter(type, pywikibot_family_classproperty_getattr)


autoclass_content = 'both'
autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'special-members': False,
    'show-inheritance': True,
}
