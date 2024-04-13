# models

> contains the schemas defining the various data handled by acme-widgets

## development

### install

```shell
# install all dependencies
poetry install --with dev
```

### make commands

several commands are provided to assist you with component development

```shell
# run this prior to pushing commits
make validate

# apply formatting and standards enforcement
make fmt-apply

# you can run the individual commands that make up 'validate' to focus on particular aspects

# run all unit tests
make test

# ensure your changes are compliant with common standards
make lint

# verify coverage standards are met
make cover

# same as above, but with browser UI showing much more detail
make cover-html
```
