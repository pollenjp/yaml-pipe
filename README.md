# yaml-pipe

## Expected Behavior

```yml
---
foo:
  bar: Hello
````

```sh
cat sample.yml | yamlpipe foo.bar="World" | cat
```

```txt
foo:
  bar: World
```
