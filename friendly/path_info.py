"""path_info.py

In many places, by default we exclude the files from this package,
thus restricting tracebacks to code written by the users.

If Friendly-traceback is used by some other program,
it might be desirable to exclude additional files.
"""
import os
import asttokens  # Only use it to find site-packages

EXCLUDED_FILE_PATH = set()
EXCLUDED_DIR_NAMES = set()
SITE_PACKAGES = os.path.abspath(os.path.join(os.path.dirname(asttokens.__file__), ".."))
FRIENDLY = os.path.abspath(os.path.dirname(__file__))
TESTS = os.path.abspath(os.path.join(FRIENDLY, "..", "tests"))


def exclude_file_from_traceback(full_path):
    """Exclude a file from appearing in a traceback generated by
    Friendly-traceback.  Note that this does not apply to
    the true Python traceback obtained using "debug_tb".
    """
    if not os.path.isfile(full_path):
        raise RuntimeError(
            f"{full_path} is not a valid file path; it cannot be excluded."
        )
    # full_path could be a pathlib.Path instance
    full_path = str(full_path)
    EXCLUDED_FILE_PATH.add(full_path)


def exclude_directory_from_traceback(dir_name):
    """Exclude all files found in a given directory, including sub-directories,
    from appearing in a traceback generated by Friendly.
    Note that this does not apply to the true Python traceback
    obtained using "debug_tb".
    """
    if not os.path.isdir(dir_name):
        raise RuntimeError(f"{dir_name} is not a directory; it cannot be excluded.")
    # dir_name could be a pathlib.Path instance.
    dir_name = str(dir_name)
    # Suppose we have dir_name = "this/path" instead of "this/path/".
    # Later, when we want to exclude a directory, we get the following file path:
    # "this/path2/name.py". If we don't append the ending "/", we would exclude
    # this file by error in is_excluded_file below.
    if dir_name[-1] != os.path.sep:
        dir_name += os.path.sep
    EXCLUDED_DIR_NAMES.add(dir_name)


dirname = os.path.abspath(os.path.dirname(__file__))
exclude_directory_from_traceback(dirname)


def is_excluded_file(full_path):
    """Determines if the file belongs to the group that is excluded from tracebacks."""
    if full_path.startswith("<frozen "):
        return True
    # full_path could be a pathlib.Path instance
    full_path = str(full_path)
    for dirs in EXCLUDED_DIR_NAMES:
        if full_path.startswith(dirs):
            return True
    return full_path in EXCLUDED_FILE_PATH


def include_file_in_traceback(full_path):
    """Reverses the effect of ``exclude_file_from_traceback()`` so that
    the file can potentially appear in later tracebacks generated
    by Friendly-traceback.

    A typical pattern might be something like::

         import some_module

         revert = not is_excluded_file(some_module.__file__)
         if revert:
             exclude_file_from_traceback(some_module.__file__)

         try:
             some_module.do_something(...)
         except Exception:
             friendly.explain_traceback()
         finally:
             if revert:
                 include_file_in_traceback(some_module.__file__)

    """
    EXCLUDED_FILE_PATH.discard(full_path)


class PathUtil:
    def __init__(self):
        self.python = os.path.abspath(os.path.dirname(os.__file__))
        self.home = os.path.expanduser("~")

    def shorten_path(self, path):  # pragma: no cover
        if path is None:  # can happen in some rare cases
            return path
        path = path.replace("'", "")  # We might get passed a path repr
        path = os.path.abspath(path)
        path_lower = path.lower()

        if "<SyntaxError>" in path:  # with IDLE's latest hack
            # see https://bugs.python.org/issue43476
            path = "<SyntaxError>"
        elif "<pyshell#" in path:
            path = "<pyshell#" + path.split("<pyshell#")[1]
        elif "<ipython-input-" in path:
            parts = path.split("<ipython")
            parts = parts[1].split("-")
            path = "[" + parts[-2] + "]"
        elif "<friendly-console:" in path:
            path = "<friendly-console:" + path.split("<friendly-console:")[1]
        elif path_lower.startswith(SITE_PACKAGES.lower()):
            path = "LOCAL:" + path[len(SITE_PACKAGES) :]
        elif path_lower.startswith(self.python.lower()):
            path = "PYTHON_LIB:" + path[len(self.python) :]
        elif path_lower.startswith(FRIENDLY.lower()):
            path = "FRIENDLY:" + path[len(FRIENDLY) :]
        elif path_lower.startswith(TESTS.lower()):
            path = "TESTS:" + path[len(TESTS) :]
        elif path_lower.startswith(self.home.lower()):
            path = "HOME:" + path[len(self.home) :]
        return path


path_utils = PathUtil()


def show_paths():  # pragma: no cover
    """To avoid displaying very long file paths to the user,
    Friendly-traceback tries to shorten them using some easily
    recognized synonyms. This function shows the path synonyms
    currently used.
    """
    print("HOME =", path_utils.home)
    print("LOCAL =", SITE_PACKAGES)
    print("PYTHON_LIB =", path_utils.python)
    if FRIENDLY != SITE_PACKAGES:
        print("FRIENDLY = ", FRIENDLY)
