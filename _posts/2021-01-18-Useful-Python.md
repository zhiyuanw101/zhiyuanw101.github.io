---
layout: post
title: Useful Python Stuff
categories: [Python, Utils, Wiki]
description: Useful Python
keywords: Python, Utils, Wiki
---

## Debugger - PDB (pdb++)

- [cheat sheet](https://kapeli.com/cheat_sheets/Python_Debugger.docset/Contents/Resources/Documents/index)

## Test - pytest

- [doc](https://docs.pytest.org/en/latest/)
  - [EECS 485 Resource](https://eecs485staff.github.io/p1-insta485-static/setup_pytest.html)
- find test: run all files of the form `test_*.py` or `*_test.py` in the current directory and its subdirectories

## `pathlib`

- [cheatsheet](https://github.com/chris1610/pbpython/blob/master/extras/Pathlib-Cheatsheet.pdf)
- [reference](https://realpython.com/python-pathlib/#examples)

### creating path

- `pathlib.Path(r'dir1/dir2')`
- `path = path1 / path2 / path3`: construct join of parts
- `path = path1.joinpath(path2, path3)`: equivalent to above
- `pathlib.Path.cwd()`: create Current Working Directory
- `pathlib.Path.home()`: create Home Directory
- `path.resolve()`: get full path
- `path.parent`: parent path

### path components

- `.name`: the file name without any directory
- `.parent`: the directory containing the file, or the parent directory if path is a directory
- `.stem`: the file name without the suffix
- `.suffix`: the file extension
- `.anchor`: the part of the path before the directories

### open files

- using `open()`

  ```python
  path = pathlib.Path.cwd() / 'tmp.md'
  with open(path, mode='r') as f:
      ...
  ```

- using `path.open()`
  
  ```python
  path = pathlib.Path.cwd() / 'tmp.md'
  with path.open(mode='r') as f:
    ...
  ```

- pathlib functions
  - .`read_text()`: open the path in text mode and return the contents as a string.
  - `.read_bytes()`: open the path in binary/bytes mode and return the contents as a bytestring.
  - `.write_text()`: open the path and write string data to it.
  - `.write_bytes()`: open the path in binary/bytes mode and write data to it.
