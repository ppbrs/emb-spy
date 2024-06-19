# emb-spy

Debugging framework for embedded systems.

# Overview

Reg-analyzer is intended for reading registers of a MCU and analyze and visualize the values.

Reg-analyzer has two layers:
1. Backend
The backend connects to OpenOCD via telnet. In the future it will probably be able to start OpenOCD itself if necessary. Then the backend reads registers as fast as possible and gives their values to the application.
2. Application

Static
analyze values, check for errors, calculate physical parameters based on register values.

Dynamic
visualize values: draw plots of values over time

Script
Set some registers in some sequence

# Building instructions (for the maintainer)

Run this command in the directory where `pyproject.toml` is located.
```
python3 -m build
```
Two files will be created in the `dist` directory:
```
dist/
├── emb_spy-0.0.1-py3-none-any.whl
└── emb_spy-0.0.1.tar.gz
```
The tar.gz file is a source distribution whereas the .whl file is a built distribution.

## Uploading the project to test.pypi.org

To securely upload the package, a token with a `pypi-` prefix must be generated at (https://test.pypi.org/manage/account/#api-tokens). Use that token to upload all the archives under `dist`:
```
python3 -m twine upload --repository testpypi dist/*
```
For the username, use __token__. For the password, use the token value.
Once uploaded, check if the application is accessible at (https://test.pypi.org/project/emb-spy/0.0.1/).
Now you can check that the application can be installed and it works.
```
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps emb-spy
```

## Uploading the project to pypi.org

(placeholder)
