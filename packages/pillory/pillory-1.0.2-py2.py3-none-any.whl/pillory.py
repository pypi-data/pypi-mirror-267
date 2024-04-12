"""
A linter to scrutinize how you are using mocks in Python.
"""

__version__ = "1.0.2"

import ast
import importlib
import pathlib
import sys
import types
from collections.abc import Iterator

# Excludes taken from ruff.
EXCLUDE = [
    ".bzr",
    ".direnv",
    ".eggs",
    ".git",
    ".git-rewrite",
    ".hg",
    ".ipynb_checkpoints",
    ".mypy_cache",
    ".nox",
    ".pants.d",
    ".pyenv",
    ".pytest_cache",
    ".pytype",
    ".ruff_cache",
    ".svn",
    ".tox",
    ".venv",
    ".vscode",
    "__pypackages__",
    "_build",
    "buck-out",
    "build",
    "dist",
    "node_modules",
    "site-packages",
    "venv",
]


def walk_path(path: pathlib.Path) -> Iterator[pathlib.Path]:
    if path.is_dir() and str(path) not in EXCLUDE:
        for item in path.iterdir():
            yield from walk_path(item)
    else:
        yield path


class MockImportVisitor(ast.NodeVisitor):
    def __init__(self):
        self.patches = []

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name) and node.func.id == "patch":
            self.patches.append(node)
        elif isinstance(node.func, ast.Attribute) and node.func.attr == "patch":
            self.patches.append(node)


def import_or_getattr(target, current=None):
    if "." in target:
        first, rest = target.split(".", 1)
    else:
        first = target
        rest = None
    try:
        found = getattr(current, first)
    except AttributeError:
        if not current:
            found = importlib.import_module(first)
        else:
            found = importlib.import_module(f"{current.__name__}.{first}")
    if rest:
        return import_or_getattr(rest, current=found)
    return found


RULE_MESSAGES = {
    "PM101": "patched implementation",
    "PM102": "patched is not a top level module attribute",
    "PM103": "patched builtins instead of module under test",
}


def find_errors(source):
    try:
        parsed = ast.parse(source)
    except Exception:
        return
    visitor = MockImportVisitor()
    visitor.visit(parsed)
    for node in visitor.patches:
        arg = node.args[0].value
        target, attribute = arg.rsplit(".", 1)
        if target == "builtins":
            yield ("PM103", node.lineno, node.col_offset, arg)
            continue
        value = import_or_getattr(target)
        patched = getattr(value, attribute)
        if not isinstance(value, types.ModuleType):
            yield ("PM102", node.lineno, node.col_offset, arg)
        elif patched.__module__ == target:
            yield ("PM101", node.lineno, node.col_offset, arg)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] != ".":
        starting_files = list(pathlib.Path(".").glob(sys.argv[1]))
    else:
        starting_files = [pathlib.Path(".")]
    files = [file for path in starting_files for file in walk_path(path)]
    for file in files:
        try:
            source = file.read_text()
        except Exception:
            continue
        for rule_code, lineno, col_offset, arg in find_errors(source):
            print(
                f"{file}:{lineno}:{col_offset}: {rule_code} {RULE_MESSAGES[rule_code]} {arg}"
            )
