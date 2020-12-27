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

### Exercise

1. man ls

    ```sh
    ls -lAaGht
    -A: all except ../ .
    -a: include ../ .
    -G: print color
    -h: use unit suffixes: Byte, KB...
    -t: sort by last modified
    ```

2. marco, polo

    ```sh
    marco () {
        export MCD=$(pwd)
        echo "MCD is set to ${MCD}"
    }

    polo () {
        cd ${MCD}
        echo ${MCD}
        }
    ```

3. random test with counter

    - notice difference between `sh xx.sh/ source xx.sh/ . ./source.sh`
    - notice implementation of [counter](https://www.baeldung.com/linux/bash-script-counter)
    - [if](https://thoughtbot.com/blog/the-unix-shells-humble-if)
    - [comparison, test](http://mywiki.wooledge.org/BashFAQ/031)
  
    ```sh
    #!/bin/sh
  
    counter=0
    while true; do
        echo "num: $counter"
        sh random.sh
        if [ $? -eq 1 ]; then
            echo random\ script\ exit with error
            break
        fi
        echo random\ script\ run\ successfully
        let counter++
    done
    echo done!
    ```

4. [`xargs`](https://www.man7.org/linux/man-pages/man1/xargs.1.html)

    - `xargs`: execute a command using STDIN as arguments
      - `-0`: input null character as a separator
      - `-t`: print command executed
      - `-p`: print command to be execute
      - `-Istr`: replace `str` initial-arguments with names read from standard input.
    - [`find`](https://man7.org/linux/man-pages/man1/find.1.html):
      - `find [starting-point...] [expression]`
      - `[expression]`:
        - Tests
          - `-true`: find all
          - `-name PATTERN`
          - `-perm -MODE`/`-perm /MODE`: 
        - Actions
          - `-print`: by default
          - `-print0`
          - `-ok COMMAND`: like `-exec` but ask first
          - `-exec COMMAND`: `{}` replaced by current filename being processed
        - Global options
          - `-maxdepth LEVELS`: Descend at most LEVELS (a non-negative integer)
        - Positional options
        - Operators: often replace `(`, `!` with `\(`, `\!`
          - `( expr )`
          - `! expr`/ `-not expr`
          - `expr1 -a expr2`/ `expr1 -and expr2`/ `expr1 expr2`
          - `expr1 -o expr2`/ `expr1 -or expr2`
      - `-exec`: `{}` as the founded DIR, end with \; or ";"
      - `-print0`: print result followed by a null character, corresponds to the -0 option of xargs.
  
    ```sh
    # GNU find: gfind
    gfind . -name "*.sh" -exec echo {} \; | xargs zip sh.zip 
    gfind . -name "*.sh" -print0 | xargs -0 zip sh.zip
    ```