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
  - `"$VAR"` will be substituted
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

### [Regex](https://regexone.com/)

[Regex debugger](https://regex101.com/)

- `.`: any single character
- `\d`: Any digit, `\D`: any none digit
- `\w`: any alphanumeric character, `\W`: any non-alphanumeric character
- `[abc]/ [a-c]`: single character in a,b,c
- `{m}`: m repititions
- `*`: zero or more repititions
- `+`: one or more repititions
- `\s`: any whitespace (space, tab, new line/...), `\S`: any non-whitespace
- `^...&`: start and end of line
- `(...)`: capture group, `(abc|def)`: match abc or def
- `?`: optional character

### Tools

- `sort`
- `awk`
- `paste`
- `wc`
- `R`
- `bc`
- `gnuplot`

### Excerise

1. [Regex](https://regexone.com/)
2. Find the number of words (in `/usr/share/dict/words`) that contain at least three `a`s and don’t have a `'s` ending. What are the three most common last two letters of those words? `sed`’s y command, or the `tr` program, may help you with case insensitivity. How many of those two-letter combinations are there? And for a challenge: which combinations do not occur?

  ```sh
 head -n 20 /usr/share/dict/words | \
 tr "[A-Z]" "[a-z]" | \
 sed -E 's/((^(\w*a\w*){3}([^'][a-zA-Z]|[a-zA-Z'][^s])$|^(\w*a\w*){2}(a\w|[a-zA-Z']a)$)|.*)/\2/'
  ```

  ```sh
  cat /usr/share/dict/words | \
  grep '.\+.\+' | \
  sed -E 's/^.*(..)$/\1/' | \
  sort | \
  uniq -c | \
  sort -nk1,1 | \
  tail -n 3
  ```

  ```sh
  cat /usr/share/dict/words | \
  grep '.\+.\+' | \
  sed -E 's/^.*(..)$/\1/' | \
  sort | \
  uniq -c | \
  wc -l
  ```

3. To do in-place substitution it is quite tempting to do something like `sed s/REGEX/SUBSTITUTION/ input.txt > input.txt`. However this is a bad idea, why? Is this particular to `sed`? Use `man sed` to find out how to accomplish this.

  ```sh
  sed -i '' 's/find/replace/g' filename
  ```

4. Find your average, median, and max system boot time over the last ten boots. Use `journalctl` on Linux and `log show` on macOS, and look for log timestamps near the beginning and end of each boot. 

```sh
log show | egrep '=== system boot:|Previous shutdown cause:'
```

## Lec 5: Command-line Environment

### Job Control

- `SIGINT`: `Ctrl-C`
- `SIGQUIT`: `Ctrl-\`
- `SIGTERM`: `kill -TERM %job-id`
- `SIGSTP/SIGSTOP`: `Ctrl-Z`
- `jobs`: show all jobs
- `COMMAND &`: run in backgrounds
- `bg`: continue stopped job in background
- `fg`: continue stopped job in prompt
- `kill`: signal a process
  - `kill -l`: list all signals
  - `kill -(signal_name|signal_number) (pid|%job_id)`
    - process can be referred to by pid or job_id

### [Terminal Multiplexers (tmux)](https://tmuxcheatsheet.com/)

[tutorial](https://www.hamvocke.com/blog/a-quick-and-easy-guide-to-tmux/)
[customization](https://www.hamvocke.com/blog/a-guide-to-customizing-your-tmux-conf/)

#### Session

- `$ tmux -s mysession`: start new session named myssion
- `$ tmux ls`: list all sessions
- `$ tmux a -t mysession`: attatch to mysession
- `C-b d`: detach current session
- `C-b $`: rename session
- `C-b s`: list sessions

#### Windows

- `C-b c`: create window
- `C-b &`: close current window
- `C-b p`: previous window
- `C-b n`: next window
- `C-b 1...9`: select window by number

#### Panels

- `C-b ;`: last active panel
- `C-b %`: split vertically
- `C-b "`: split horizontally
- `C-b z`: zoom panel
- `C-b !`: convert panel into window

### Dotfiles

- bash - `~/.bashrc, ~/.bash_profile`
- git - `~/.gitconfig`
- vim - `~/.vimrc and the ~/.vim folder`
- ssh - `~/.ssh/config`
- tmux - `~/.tmux.conf`

using soft-link, source at `~/Configs/`, remote at `git@github.com:zhiyuanw101/Dotfiles-Configs.git`

### ssh

#### [ssh forwarding](https://zhiyuanw101.github.io/2021/01/08/SSH-Forwarding/)
#### utils
- [mosh](https://mosh.org/)
- [sshfs](https://github.com/libfuse/sshfs)
### Excercise

1. From what we have seen, we can use some `ps aux | grep` commands to get our jobs’ pids and then kill them, but there are better ways to do it. Start a `sleep 10000` job in a terminal, background it with `Ctrl-Z` and continue its execution with bg. Now use [`pgrep`](https://www.man7.org/linux/man-pages/man1/pgrep.1.html) to find its pid and `pkill` to kill it without ever typing the pid itself. (Hint: use the `-af` flags).
2. Say you don’t want to start a process until another completes, how you would go about it? In this exercise our limiting process will always be `sleep 60 &`. One way to achieve this is to use the [`wait`](https://www.man7.org/linux/man-pages/man1/wait.1p.html) command. Try launching the sleep command and having an `ls` wait until the background process finishes.
However, this strategy will fail if we start in a different bash session, since wait only works for child processes. One feature we did not discuss in the notes is that the kill command’s exit status will be zero on success and nonzero otherwise. kill -0 does not send a signal but will give a nonzero exit status if the process does not exist. Write a bash function called pidwait that takes a pid and waits until the given process completes. You should use sleep to avoid wasting CPU unnecessarily.


## Lec 4: Git

### Data model

```c++
// a file is a bunch of bytes
type blob = array<byte>

// a directory contains named files and directories
type tree = map<string, tree | blob>

// a commit has parents, metadata, and the top-level tree
type commit = struct {
    parent: array<commit>
    author: string
    message: string
    snapshot: tree
}

// Objects
type object = blob | tree | commit

objects = map<string, object>

// SHA-1 hash for id
def store(object):
    id = sha1(object)
    objects[id] = object

def load(id):
    return objects[id]

// References
references = map<string, string>

def update_reference(name, id):
    references[name] = id

def read_reference(name):
    return references[name]

def load_reference(name_or_id):
    if name_or_id in references:
        return load(references[name_or_id])
    else:
        return load(name_or_id)
```

### Interface

- `git cat-file -p <hash-id>`: Pretty-print the contents of \<object\> based on its type.

#### Basics

- `git help <command>`: get help for a git command
- `git init`: creates a new git repo, with data stored in the .git directory
- `git status`: tells you what’s going on
- `git add <filename>`: adds files to staging area
- `git commit`: creates a new commit.
- `git log`: shows a flattened log of history
- `git log --all --graph --decorate`: visualizes history as a DAG
- `git diff <filename>`: show changes you made relative to the staging area
- `git diff <revision> <filename>`: shows differences in a file between snapshots
- `git checkout <revision>`: updates HEAD and current branch
- `git checkout <file>`: discard file changes in workspace

#### Branching and merging

- `git branch`: shows branches
- `git branch <name>`: creates a branch
- `git checkout -b <name>`: creates a branch and switches to it
  - same as `git branch <name>`; `git checkout <name>`
- `git merge <revision>`: merges into current branch
- `git mergetool`: use a fancy tool to help resolve merge conflicts
- `git rebase`: rebase set of patches onto a new base

#### Remotes

- `git remote`: list remotes
- `git remote add <name> <url>`: add a remote
- `git push <remote> <local branch>:<remote branch>`: send objects to remote, and update remote reference
- `git branch --set-upstream-to=<remote>/<remote branch>`: set up correspondence between local and remote branch
- `git fetch`: retrieve objects/references from a remote
- `git pull:` same as git fetch; git merge
- `git clone`: download repository from remote

#### Undo

- `git commit --amend`: edit a commit’s contents/message
- `git reset HEAD <file>`: unstage a file
- `git checkout -- <file>`: discard changes

#### Advanced Git

- `git config`: Git is highly customizable
- `git clone --depth=1`: shallow clone, without entire version history
- `git add -p`: interactive staging
- `git rebase -i`: interactive rebasing
- `git blame`: show who last edited which line
- `git stash`: temporarily remove modifications to working directory
- `git bisect`: binary search history (e.g. for regressions)
- `.gitignore`: specify intentionally untracked files to ignore