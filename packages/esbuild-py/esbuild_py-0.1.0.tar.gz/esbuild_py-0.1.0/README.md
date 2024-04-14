# esbuild-py

:warning: Work in progress

## Setup

Create conda environment

```sh
conda create -n esbuild-py python=3.11
```

## Build

```sh
conda activate esbuild-py
cd esbuild_py
go get github.com/keller-mark/esbuild-py
# go build -buildmode=c-shared -o _esbuild.so
```

## Develop

Build python package and install in editable mode

```sh
python setup.py bdist_wheel
python setup.py sdist
pip install -e .
python
```

```python
from esbuild_py import transform
jsx = """
import * as React from 'react'
import * as ReactDOM from 'react-dom'

ReactDOM.render(
    <h1>Hello, world!</h1>,
    document.getElementById('root')
);
"""
print(transform(jsx))
```

## Resources


- Install go v1.20.12 from https://go.dev/dl/
- https://github.com/ardanlabs/python-go/tree/master/pyext
- https://pkg.go.dev/github.com/evanw/esbuild@v0.20.2/pkg/api#hdr-Transform_API
- https://github.com/evanw/esbuild/blob/main/.github/workflows/ci.yml
