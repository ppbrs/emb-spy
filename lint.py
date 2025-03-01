"""
Run linters as regular tests.
"""

import logging
import pathlib
import subprocess

import pytest

_logger = logging.getLogger(__name__)


def _get_all_python_modules() -> list[str]:
    """
    Return a list of paths all python modules.

    The output function must be determenistic because it will be used by both 'argvalues' and 'ids'
    of the same pytest.parametrize decorator.

    This function outputs strings instead of pathlib.Path because there is no value in those as
    they would have been converted to strings anyways.
    """
    attr_name = "cache"
    if not hasattr(_get_all_python_modules, attr_name):
        cwd = pathlib.PosixPath.cwd()
        cache = list(str(path.relative_to(cwd)) for path in cwd.rglob("*.py"))
        setattr(_get_all_python_modules, attr_name, cache)
    return getattr(_get_all_python_modules, attr_name)


@pytest.mark.parametrize(
    argnames="path", argvalues=_get_all_python_modules(), ids=_get_all_python_modules()
)
def test_lint_ruff_format(
    path: str,
) -> None:
    """Check that a python module is properly formatted."""
    completed_process = subprocess.run(
        f"ruff format --diff '{path}'",
        shell=True,
        check=False,
        capture_output=True,
        text=True,
    )
    for line in completed_process.stdout.splitlines():
        if line:
            _logger.info(line)
    if completed_process.returncode != 0:
        for line in completed_process.stderr.splitlines():
            _logger.error(line)
        assert False, f"Ruff thinks '{path}' needs reformatting."


@pytest.mark.parametrize(
    argnames="path", argvalues=_get_all_python_modules(), ids=_get_all_python_modules()
)
def test_lint_isort(
    path: str,
) -> None:
    """Check that imports in this python module are properly sorted and formatted."""
    completed_process = subprocess.run(
        f"isort {path} --check",
        shell=True,
        check=False,
        capture_output=True,
        text=True,
    )
    if completed_process.returncode != 0:
        for line in completed_process.stderr.splitlines():
            _logger.error("%s", line)
        assert False, "isort failed"
