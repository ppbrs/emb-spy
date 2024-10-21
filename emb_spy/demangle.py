
# import cpp_demangle  # https://github.com/benfred/py-cpp-demangle

# def demangle(name):
#     return cpp_demangle.demangle(name)

import subprocess as sp


def demangle(name: str) -> str:
    child = sp.Popen(args=["c++filt", name], stdout=sp.PIPE, stderr=None)
    outs_b, _ = child.communicate()
    exit_code = child.wait()
    outs = outs_b.decode(encoding="ascii", errors="ignore").split("\n")
    if exit_code != 0:
        raise ValueError
    return outs[0]
