---
layout: post
title: CS missing course
categories: [Utils, Wiki]
description: CS missing course
keywords: Utils, Wiki
---
**[./missing-semester](https://missing.csail.mit.edu/)**

## [Lec 1: Course overview + the shell](https://missing.csail.mit.edu/2020/course-shell/)

- `echo hello\ world`, `echo "hello world"`: white spaces between arguments
- `sudo su`: start a super user terminal
- `#`: run in super user
- `tee FILE`: write to FILE and stdout
- `xrg-open / open FILE`: open file
- `chmod`:
  - direct mode: `chmod 777 FILE`
    - 4 for read
    - 2 for write
    - 1 for execute
  - symbolic mode: `chmod u+x FILE`
    - mode: clause [, clause ...]
    - clause: [who ...] [action ...] action
    - who: a $\vert$ u $\vert$ g $\vert$ o
    - action: op [perm ...]
    - op: + $\vert$ - $\vert$ =
    - perm: r $\vert$ s $\vert$ t $\vert$ w $\vert$ x $\vert$ X $\vert$ u $\vert$ g $\vert$ o
  - Example:
    - `755`: `u=rwx,go=rx`/ `u=rwx,go=u-w`
- **Shebang**:
  - `#!interpreter [optional-arg]`
  - use `env`
- `cut`:
  - cuts out selected portions of each line (as specified by list) from each file and writes them to the standard output. If file not specified, read from standard input.

## [Lec2: Shell Tools and Scripting](https://missing.csail.mit.edu/2020/shell-tools/)

### Scripting

- define variables
- strings: `"$foo" / '$foo'`
  - `'$ VAR'` will be substituted
- functions:
  - `source mcd.sh`
  - `mcd test`
  - difference with script
- exit code
- `$( CMD )`: *command substitution*, get output of command as variable
- `<( CMD )`: *process substitution*: execute CMD and place the output in a temporary file and substitute the `<()` with that file’s name.
- for loop:
- if
  - [test](https://www.man7.org/linux/man-pages/man1/test.1.html)
- shell globbing: `mv *.{.py,.sh} FOLDER`
  - Wildcards: `*.py`, `?.sh`
  - Curly braces: `{.png,.jpg}`, `{a..h}`

### Shell tools

- `man` and `tldr`
- `find/ fd/ locate`: find files
- `grep/ rg`: find code
- `history, fzf`: find shell commands
- `tree/ nnn`: Directory Navigation
