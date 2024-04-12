# ichandbook

This project is a set of tools to support publication and maintenance of the [ICHEC technical handbook](https://git.ichec.ie/performance/ichec-handbook). It may be useful for maintaining other technical projects too.

# Running Tests

In a Python virtual environment do:

```sh
pip install .'[test]'
```

## Unit Tests

```sh
pytest
```

## Linting and Static Analysis

```sh
black src test
mypy src test
```

## All Tests

Requires `tox`:

```sh
tox
```


