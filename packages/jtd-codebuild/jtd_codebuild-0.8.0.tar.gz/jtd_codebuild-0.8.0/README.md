# JSON Type Definition Code Build

[![PyPI version](https://badge.fury.io/py/jtd-codebuild.svg)](https://pypi.org/project/jtd-codebuild)
[![Testsuite](https://github.com/01Joseph-Hwang10/jtd-codebuild/workflows/Test%20and%20Lint/badge.svg)](https://github.com/01Joseph-Hwang10/jtd-codebuild/actions?query=workflow%3A"Test+and+Lint")
[![Python version](https://img.shields.io/pypi/pyversions/jtd-codebuild.svg)](https://pypi.org/project/jtd-codebuild)
[![Project Status](https://img.shields.io/pypi/status/jtd-codebuild.svg)](https://pypi.org/project/jtd-codebuild/)
[![Supported Interpreters](https://img.shields.io/pypi/implementation/jtd-codebuild.svg)](https://pypi.org/project/jtd-codebuild/)
[![License](https://img.shields.io/pypi/l/jtd-codebuild.svg)](https://github.com/pawelzny/jtd-codebuild/blob/master/LICENSE)

jtd-codebuild is a tool for generating language specific schemas and interfaces code from JSON Type Definition IDL files in either yaml or json format.

This tool is built on top of [`jtd-codegen`](https://jsontypedef.com/) so check out the documentation if you don't have a clue about JSON Type Definition.

## Prerequisites

- [jtd-codegen](https://jsontypedef.com/docs/jtd-codegen/)

## Installation

```bash
pip install jtd-codebuild
```

## Usage

First, you need to create a configuration file named `jtd-codebuild.json` in the root of your project. (See [Configuration](#configuration))

Then, write JSON type definition IDL files in either yaml or json format in the directory you specified in the configuration file.

After all of that, you can run the command below to generate code.

```bash
jtd-codebuild path/to/the/folder/where/jtd-codebuild.json/is/located
```

### Usage Example

You can find the example project here: [jtd_codebuild/tests/fixtures/example_project_1](./jtd_codebuild/tests/fixtures/example_project_1)

Also, you can get a sense of how this tool works by looking at the test cases: [jtd_codebuild/tests/test_example_project_1.py](./jtd_codebuild/tests/test_example_project_1.py)


## Required conventions

### Configuration

The script will find `jtd-codebuild.json` which is the configuration file of this tooling.

#### `root-schema-path`

The path to the root schema file. 
Root schema file will be the entry point of the code generation, 
where every definition files will be merged into.

Defaults to `schema.jtd.yaml`

#### `definitions-path` (alias: `definitions-paths`)

The path to single or multiple definition files.
This directory will be recursively searched for definition files.

Definition file is a file that contains a single or multiple definitions.
Checkout the documentation below for more information.

Defaults to `[]`

#### `output-schema-path`

The path for the merged schema file converted in json format.

Defaults to `gen/schema.jtd.json`

#### `includes`

Array of JTD package paths to include.

The path should have `jtd-codebuild.json` file in it 
so that this tool can find the codebuild configuration.

If you specifiy a package path,
it will reference the package's schema definitions 
when generating schema file you are working on.

Defaults to `[]`

#### `allow-duplicate-defs`

Whether to allow duplicate definitions.

This only applies to the definitions that are not in the same jtd codebuild project.

That is, definitions in `definitions-path` in each project always raises error if there are duplicate definitions.

Defaults to `false`

#### `targets`

Compile targets.

Defaults to `[]`

It's a JSONRecord contains the object having following properties:
  - `language (string)`: The language of the target.
                We essentially inject this value to `jtd-codegen` as target language option
                which is provided as a flag which is like `--{language}-out`.
                Available languages can be found in the documentation of `jtd-codegen`. 
                (See: https://jsontypedef.com/)
  - `path (string)`: The path to the directory where the generated code will be placed.

##### `targets` - Language Specific Options - Python

- `use-pydantic (boolean)`: Whether to use pydantic as a `dataclass` decorator provider.
                            If this is set to true, the generated code will use `pydantic.dataclasses.dataclass` as a `dataclass` decorator so that you can use pydantic's validation features.
                            Otherwise, the generated code will be plain python dataclasses.
                            Defaults to `false`.
- `use-typeddict (boolean)`: Whether to use `TypedDict` instead of `dataclass`.
                             If this is set to true, the generated code will use `TypedDict` instead of `dataclass`. This property cannot be set to true if `use-pydantic` is set to true. Also, subscriptable option will be ignored if this is set to true.
- `property-case (enum)`: The case of the property names.
                          This property is only effective when `use-typeddict` is set to true.
                          Available values are `snake` and `camel`.
                          Defaults to `snake`.
- `subscriptable (boolean)`: Whether to make the generated class subscriptable.
                            If this is set to true, the generated class will be subscriptable so that you can access the properties of the class like `obj["property"]`.
                            Otherwise, the generated class will not be subscriptable.
                            Defaults to `false`.

##### `targets` - Language Specific Options - TypeScript

- `tsconfig-path (string)`: The path to the tsconfig file.
                            This will be used to compile typescript code 
                            to javascript code and type declarations.
                            If you want to automatically generate 
                            plain javascript artifact with type declarations, 
                            you should also provide this option.


### Configuration Example

Example congfiguration file is provided below. Copy it and modify it to your needs.

```jsonc
{
  "root-schema-path": "schema.jtd.yaml",
  "definitions-path": "definitions",
  "output-schema-path": "gen/schema.jtd.json",
  "includes": ["../path/to/another/folder/that/contains/jtd-codebuild.json"],
  "targets": [
    {
      "language": "python",
      "path": "gen/python"
    },
    {
      "language": "python",
      "path": "gen/python-pydantic",
      "use-pydantic": true,
      "subscriptable": true
    },
    {
      "language": "python",
      "path": "gen/python-typeddict",
      "use-typeddict": true,
      "subscriptable": true
    },
    {
      "language": "typescript",
      "path": "gen/typescript",
      "tsconfig-path": "tsconfig.build.json"
    }
  ]
}
```

### Root Schema File

Root schema file is the entry point of the code generation. 

It will be the file where every definition files will be merged into.

If you don't need a root `Schema` type, you can just create an empty file.

### Definition files

Definition files are sharable files of which each of them contains a single or multiple definitions.

Each declared keys as a root key in the definition file will be merged as a key of `definitions` object in the root schema file, and those symbols can be shared across the other definition files.

For example, let's say you have a definition file whose code is like below.

```yaml
book:
  properties:
    id:
      type: string
    title:
      type: string
```

This can be referenced in other definition files like below.

```yaml
user:
  properties:
    id:
      type: string
    name:
      type: string
    books:
      elements:
        ref: book
```

This will be merged as a single schema like below.

```json
{
  "definitions": {
    "book": {
      "properties": {
        "id": {
          "type": "string"
        },
        "title": {
          "type": "string"
        }
      }
    },
    "user": {
      "properties": {
        "id": {
          "type": "string"
        },
        "name": {
          "type": "string"
        },
        "books": {
          "elements": {
            "ref": "book"
          }
        }
      }
    }
  }
}
```

Checkout more about `ref` if you don't have a clue about it. https://jsontypedef.com/docs/jtd-in-5-minutes/#ref-schemas

### Inheritance

`jtd-codebuild` supports inheritance between type definitions.

You can do this by using `extends` keyword like below.

```yaml
Person:
  properties:
    id:
      type: string
    name:
      type: string

Chef:
  extends: Person
  properties:
    restaurant:
      type: string

HeadChef:
  extends: Chef
  properties:
    sousChef:
      ref: Chef
```

You can also extend multiple types like below.

```yaml
Person:
  properties:
    id:
      type: string
    name:
      type: string

MyRestaurantMixin:
  properties:
    restaurant:
      type: string

Chef:
  extends: [Person, MyRestaurantMixin]
```

### Manual dependency management

Since IDL files are basically just a bunch of JSON objects,
we need to manually manage the dependency between the definition files.

For example, assume you have a folder structure like the below:

```
definitions
├── book
│   └── book.jtd.yaml
└── user
    └── user.jtd.yaml
```

And assume that `book.jtd.yaml` and `user.jtd.yaml` are the root definition files of each module.

In this case, you need to annotate that `user.jtd.yaml` depends on `book.jtd.yaml` like below.

```yaml
# user.jtd.yaml
#
# Depends on:
#   - book (at ../book/book.jtd.yaml)
user:
  properties:
    id:
      type: string
    name:
      type: string
    books:
      elements:
        ref: book
```

## Contributing

Any contribution is welcome! Check out [CONTRIBUTING.md](https://github.com/01Joseph-Hwang10/jtd-codebuild/blob/master/.github/CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](https://github.com/01Joseph-Hwang10/jtd-codebuild/blob/master/.github/CODE_OF_CONDUCT.md) for more information on how to get started.

## License

`jtd-codebuild` is licensed under a [MIT License](https://github.com/01Joseph-Hwang10/jtd-codebuild/blob/master/LICENSE).
