---
layout: post
title: CS missing course
categories: [Utils, Wiki]
description: CS missing course
keywords: Utils, Wiki
---
**[./missing-semester](https://missing.csail.mit.edu/)**

## Lec 1: Course overview + the shell [🔗](https://missing.csail.mit.edu/2020/course-shell/)

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

## Lec2: Shell Tools and Scripting [🔗](https://missing.csail.mit.edu/2020/shell-tools/)

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
- `fasd`: Directory Navigation with frequency
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

## Lec 3: Vim [🔗](https://missing.csail.mit.edu/2020/editors/)

### vimtutor

```vim
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                   Lesson 1 SUMMARY

  1. The cursor is moved using either the arrow keys or the hjkl keys.
     h (left)    j (down)       k (up)        l (right)

  2. To start Vim from the shell prompt type:  vim FILENAME <ENTER>

  3. To exit Vim type:      <ESC>   :q!    <ENTER>  to trash all changes.
              OR type:      <ESC>   :wq    <ENTER>  to save the changes.

  4. To delete the character at the cursor type:  x

  5. To insert or append text type:
     i   type inserted text   <ESC>         insert before the cursor
     a   type appended text   <ESC>         append after the cursor
     A   type appended text   <ESC>         append after the line


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                   Lesson 2 SUMMARY


  1. dw   - To delete from the cursor up to the next word 
     d$   - To delete from the cursor to the end of a line
     dd   - To delete a whole line

  2. 2w   - To repeat a motion prepend it with a number
  3. The format for a change command is:
               operator   [number]   motion
     where:
       operator - is what to do, such as  d  for delete
       [number] - is an optional count to repeat the motion
       motion   - moves over the text to operate on, such as  w (word), $ (to the end of line), etc.

  4. 0   - To move to the start of the line 
     $   - move to end of line
     ^   - move to first none space character

  5. u        - To undo previous actions, 
     U        - To undo all the changes on a line
     CTRL-R   - To undo the undo's

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                   Lesson 3 SUMMARY


  1. p    - paste after the cursor
  
  2. r    - replace character under cursor

  3. c    - change from cursor to motion. The format for change is:

     c   [number]   motion

     ce    - change from the cursor to end of word
     c$    - change to end of line


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                   Lesson 4 Traversing/ Searching in file


  1. CTRL-G       - displays your location in the file and the file status
     G            -  moves to the end of the file
     number  G    - moves to that line number
     gg           - moves to the first line

  2. / phrase       - searches FORWARD for the phrase
     ? phrase       - searches BACKWARD for the phrase
     n/N            - After search, find the next occurrence in the same/opposite direction
     CTRL-O/CTRL-I  - takes you back to older/newer positions

  3. % - while the cursor is on a (,),[,],{, or } goes to its match

  4. :s/old/new         - substitute new for the first old in a line type    
     :s/old/new/g       - substitute new for all 'old's on a line type
     :#,#s/old/new/g    - substitute phrases between two line #'s type
     :%s/old/new/g      - substitute all occurrences in the file type
     :%s/old/new/gc     - ask for confirmation each time add 'c'


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                   Lesson 5 SUMMARY


  1.  :!COMMAND       - executes an external COMMAND.
      :!ls            -  shows a directory listing.
      :!rm FILENAME   -  removes file FILENAME.

  2.  :w FILENAME     - writes the current Vim file to disk FILENAME.

  3.  v  motion  :w FILENAME     - saves the Visually selected lines in FILENAME.

  4.  :r FILENAME/COMMAND     - read output from FILENAME/COMMAND and puts below the cursor position.


~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
                   Lesson 6 SUMMARY

  1. o   - open a line BELOW the cursor and start Insert mode.
     O   - open a line ABOVE the cursor.

  2. a   - insert text AFTER the cursor.
     A   - insert text after the end of the line.

  4. y   -  yanks (copies) text
     p   -  puts (pastes) it.

  5. R   - Replace mode until  <ESC>  is pressed.

  6. :set xxx   - sets the option "xxx".  Some options are:
        'ic' 'ignorecase'   ignore upper/lower case when searching
        'is' 'incsearch'    show partial matches for a search phrase
        'hls' 'hlsearch'    highlight all matching phrases
     You can either use the long or the short option name.
     Prepend "no" to switch an option off:   :set noic

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

```

## Lec 4: Data Wrangling [🔗](https://missing.csail.mit.edu/2020/data-wrangling/)

### [Regex](https://regex101.com/)

### Tools

- `sort`
- `awk`
- `paste`
- `wc`
- `R`
- `bc`
- `gnuplot`
