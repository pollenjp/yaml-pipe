# yaml-pipe

## Behavior

### example1

`sample.yml'

```yml
---
foo:
  bar: Hello
````

```sh
cat sample.yml | yamlpipe foo.bar="World" | cat
```

output

```txt
---
foo:
  bar: World
```
