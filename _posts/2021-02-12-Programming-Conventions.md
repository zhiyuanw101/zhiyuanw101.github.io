---
layout: post
title: Programming Conventions
categories: [Python, Wiki, C++]
description: Programming Conventions
keywords: Python, Wiki, C++
---

## Python style

- from PEP8

### Naming Conventions

#### Descriptive: Naming Styles

- `lowercase`
- `lower_case_with_underscores`
- `CapitalizedWords` (CapsWords)
- `mixedCase`
- `_single_leading_underscore`
  - weak "internal use" indicator
  - `from M import *` does not import objects whose names start with an underscore
- `single_trailing_underscore_`
  - used by convention to avoid conflicts with Python keyword
  - `class_`
- `__double_leading_underscore`
  - when naming a class attribute, invokes name mangling
  - inside `class FooBar`, `__boo` becomes `_FooBar__boo`

#### Function and Variable Names: `lower_case_with_underscores`

- lowercase, with words separated by underscores
- mixedCase is allowed only in contexts where that's already the prevailing style (e.g. `threading.py`), to retain backwards compatibility.

#### Class Names: `CapitalizedWords`

- Class names should normally use the CapWords convention.

#### Method Names and Instance Variables

- Use the function naming rules: lowercase with words separated by underscores as necessary to improve readability.

- Use one leading underscore only for non-public methods and instance variables.

#### Package and Module Names: `lowercase`

- Modules should have short, all-lowercase names.

#### Constants

- all capital letters with underscores separating words

#### Type Variable Names

- CapWords preferring short names: `T, AnyStr, Num`.
