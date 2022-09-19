"""Creates a version of syntax_traceback_it.rst to insert in the documentation.
"""

# When creating a new translation, you need to:
# 1. Make a copy of this file
# 2. Change the value of LANG as well as 'intro_text' so that they reflect the
#    appropriate language
# 3. Change the first line of this file so that the name of the rst file
#    is correct!


import os
import sys
import platform
this_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(this_dir, ".."))
import friendly_traceback

# Make it possible to find docs and tests source
docs_root_dir = os.path.abspath(
    os.path.join(this_dir, "..", "..", "friendly-docs")
)
assert os.path.isdir(docs_root_dir), "Separate docs repo need to exist"

LANG = "it"
friendly_traceback.install()
friendly_traceback.set_lang(LANG)
friendly_traceback.set_formatter("docs")

sys.path.insert(0, this_dir)
py_version = f"{sys.version_info.major}.{sys.version_info.minor}"

import trb_syntax_common

target = os.path.normpath(
    os.path.join(
        docs_root_dir, f"source/syntax_tracebacks_{LANG}.rst"
    )
)

intro_text = """
Friendly SyntaxError tracebacks - in italiano
=============================================

Friendly aims to provide friendlier feedback when an exception
is raised than what is done by Python.

This file contains only examples of SyntaxError and its sub-classes.
Some tests may appear to be repetitive to a human reader
but they are may be included to ensure more complete test coverage.

.. note::

     The content of this page is generated by running
     `{name}` located in the ``tests/`` directory.
     This needs to be done explicitly, independently of updating the
     documentation using Sphinx.
     On Windows, if Sphinx is installed on your computer, it is suggested
     instead to run make_trb.bat in the root directory as it will create
     similar files for all languages *and* update the documentation.

Friendly-traceback version: {friendly}
Python version: {python}

""".format(
    friendly=friendly_traceback.__version__,
    python=platform.python_version(),
    name=sys.argv[0],
)

print(f"Python version: {platform.python_version()}; Italian")

trb_syntax_common.create_tracebacks(target, intro_text)
