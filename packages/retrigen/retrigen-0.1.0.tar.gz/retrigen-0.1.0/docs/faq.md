
# FAQ


## How do I test the code?

This package comes with a test suite which you can run using implemented using [pytest].
In order to run the tests, you have to clone the repository and install the package.
This will also install the required tests dependencies
and test utilities defined in the extras_require section of the :code:`pyproject.toml`.

```bash
# clone the repository
git clone https://github.com/KennethEnevoldsen/retrigen

# install package and test dependencies
pip install -e ".[tests]"

# run all tests
python -m pytest
```

which will run all the test in the `tests` folder.

Specific tests can be run using:

```bash
python -m pytest tests/desired_test.py
```

If you want to check code coverage you can run the following:

```bash
python -m pytest --cov=src
```

## How is the documentation generated?

This package use [mkdocs] with the [material] theme to generate the documentation.

To make the documentation you can run:


```bash
# install sphinx, themes and extensions
pip install -e ".[docs]"

# generate html from documentations
make build-docs
```

If you wish to view the documentation in your browser you can run:

```bash
make docs-view
```

### Credits

This project was generated from the [Swift Python Cookiecutter] template.

[swift python cookiecutter]: https://github.com/kennethenevoldsen/swift-python-cookiecutter
[file an issue]: https://github.com/KennethEnevoldsen/retrigen/issues
[mkdocs]: https://www.mkdocs.org/getting-started/
[material]: https://squidfunk.github.io/mkdocs-material/
