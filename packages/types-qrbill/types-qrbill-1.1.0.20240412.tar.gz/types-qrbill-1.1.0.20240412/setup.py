from setuptools import setup

name = "types-qrbill"
description = "Typing stubs for qrbill"
long_description = '''
## Typing stubs for qrbill

This is a [PEP 561](https://peps.python.org/pep-0561/)
type stub package for the [`qrbill`](https://github.com/claudep/swiss-qr-bill) package.
It can be used by type-checking tools like
[mypy](https://github.com/python/mypy/),
[pyright](https://github.com/microsoft/pyright),
[pytype](https://github.com/google/pytype/),
PyCharm, etc. to check code that uses
`qrbill`.

This version of `types-qrbill` aims to provide accurate annotations
for `qrbill==1.1.*`.
The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/qrbill. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `6883b80f5286c7c8d540fa56b4fbf49364719e18` and was tested
with mypy 1.9.0, pyright 1.1.358, and
pytype 2024.3.19.
'''.lstrip()

setup(name=name,
      version="1.1.0.20240412",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/qrbill.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=['types-qrcode'],
      packages=['qrbill-stubs'],
      package_data={'qrbill-stubs': ['__init__.pyi', 'bill.pyi', 'METADATA.toml', 'py.typed']},
      license="Apache-2.0 license",
      python_requires=">=3.8",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
