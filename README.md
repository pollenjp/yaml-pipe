# yaml-pipe

<p align="center">
  <a href="https://pypi.org/project/yaml-pipe/">
    <img
      alt="PyPI Python Versions"
      src="https://img.shields.io/pypi/pyversions/yaml-pipe"
    />
  </a>
  <a href="https://pypi.org/project/yaml-pipe/">
    <img
      alt="PyPI"
      src="https://img.shields.io/pypi/v/yaml-pipe"
    />
  </a>
  <a href="https://pepy.tech/project/yaml-pipe">
    <img
      alt="Download"
      src="https://static.pepy.tech/personalized-badge/yaml-pipe?period=total&units=international_system&left_color=black&right_color=orange&left_text=Downloads"
    />
  </a>
  <a href="https://github.com/psf/black">
    <img
      alt="Issues"
      src="https://img.shields.io/badge/code%20style-black-000000.svg"
    />
  </a>
  <a href="https://github.com/pollenjp/yaml-pipe/actions/workflows/release.yml">
    <img
      alt="Release Drafter"
      src="https://github.com/pollenjp/yaml-pipe/actions/workflows/release.yml/badge.svg"
    />
  </a>
</p>

## Install

```sh
pip install yaml-pipe
```

## How to use

### example1

`sample.yml`

```yml
---
foo:
  bar: BAR
````

```sh
cat sample.yml | yaml-pipe foo.bar="bar"
```

output

```yaml
---
foo:
  bar: bar
```

### example2

`sample.yml`

```yaml
---
foo:
  bar: BAR
---
fizz:
  buzz: BUZZ
````

```sh
cat sample.yml | yaml-pipe --block_id 1 fizz.buzz="buzz"
```

output

```yaml
---
foo:
  bar: BAR
---
fizz:
  buzz: buzz
```

### example3

`sample.yml`

```yaml
---
foo:
  bar: BAR
---
fizz:
  buzz: BUZZ
````

`update.yml`

```yml
fizz:
  buzz: buzz
```

```sh
cat sample.yml | yaml-pipe --block_id 1 -f update.yml
```

output

```yaml
---
foo:
  bar: BAR
---
fizz:
  buzz: buzz
```

## Developers

### Linting and test

```sh
pyenv local 3.10.4 3.9.13 3.8.13
```

```sh
poetry install
poetry run nox
```

### Upload to PyPI

Default target is testpypi.

```sh
make pypi-upload
```

If you upload to pypi, set empty to `TEST_PYPI`.

```sh
make pypi-upload TEST_PYPI=
```
