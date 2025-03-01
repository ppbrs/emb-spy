"""
Contains a function for demangling C++ symbol names.

I used cpp_demangle library before (https://github.com/benfred/py-cpp-demangle)
which turned out to either return wrong results or throw exceptions in
some cases.
"""

import subprocess


def demangle(name: str) -> str:
    """Return demangled symbol name."""
    completed_process = subprocess.run(
        args=["c++filt", name],
        check=False,
        capture_output=True,
        text=True,
    )
    return completed_process.stdout.splitlines()[0]
