# yaml-pipe

## Install

```sh
pip install yaml-pipe
```

## How to use

### example1

`sample.yml'

```yml
---
foo:
  bar: BAR
````

```sh
cat sample.yml | yaml-pipe foo.bar="bar"
```

output

```txt
---
foo:
  bar: bar
```

### example2

`sample.yml'

```yaml
---
foo:
  bar: BAR
---
fizz:
  buzz: BUZZ
````

```sh
cat sample.yml | yaml-pipe --block_id 2 fizz.buzz="buzz"
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
