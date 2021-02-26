---
layout: post
title: Bash utils
categories: [Unix, Utils, Wiki, Shell, Bash]
description:  Bash utils
keywords: Unix, Utils, Wiki
---
## Parameter Expansion

- [link](https://wiki.bash-hackers.org/syntax/pe)

### Special parameter

- `$$`: current pid
## Expansions and substitutions

- [link](https://wiki.bash-hackers.org/syntax/expansion/intro)

## Compound commands

- [link](https://wiki.bash-hackers.org/syntax/ccmd/intro)

## `tr <string1> <string2>`

- translate characters: copies standard input to standard output with substitution or deletion of selected characters
- `tr -d '*'`: delete all `*` from input and output to stdout

## `env`

- set environment and execute command, or print environment

## `shasum`

- accept from std input/FILE, std output SHA-1(default) hash
  - `shasum -a 256 [FILE]`: generate hash

## `cmp`

- compare byte by byte

## `openssl`

- cryptography toolkit

## `test`

- condition evaluation utility, same as `[`
  - `test 001 = 1; echo $?`
  - [`test, [, [[`](http://mywiki.wooledge.org/BashFAQ/031)

## `set`

- [`set -euxo pipefail`](https://vaneyckt.io/posts/safer_bash_scripts_with_set_euxo_pipefail/)
- [doc](https://www.gnu.org/software/bash/manual/html_node/The-Set-Builtin.html)
- Display, set or unset values of shell attributes and positional parameters

## `file`

- determine file type

## `source` and execution

- `source`: execute in current shell

  ```sh
  $ source [path-to-file]
  # is equivalent to
  $ . [path-to-file]
  ```

- `./` execute: execute executable in new shell

  ```sh
  $ [path-to-executable]
  # for example, python is in $PATH
  $ python
  # executable is not in $PATH, but in current directory
  $ ./executable
  ```

## `groups`

- [reference](https://www.howtogeek.com/50787/add-a-user-to-a-group-or-second-group-on-linux/)


## Unix file
- File descriptor table
  - file descriptor as indexes
    - 0: stdin
    - 1: stdout
    - 2: stderr

### redirection

- `[n]<file`: set file as input for fd `n`
- `[n]>file`: set file as output for fd `n`
- `&>file`: set file as fd1 and fd2, overwrite
- `[a]>&[b]`: redirect fd `a` to fd `b`
  - compare with `>`: `>` is to file, `>&` to fd
- `[command] <<< "string"`: send string as stdin

## Control flow

### `for`
```sh
for var in list; do
    command
done

# inline
for file in $(ls); do echo "loop: $file"; done
```
### `while`
```sh
while test-commands; do
    command
done
```
### `until`
```sh
until test-command; do
    command
done
```
### `if-elif-else`
```sh
if test-commands; then
    command
elif test-commands; then
    command
else
    command
fi

# inline
if [[ 100 -lt 200 ]]; then echo "100 < 200"; fi
```

### test commands
#### `test expr`
- short hand: `[ expr ]`

#### `[[ expr ]]`: bash condition
- rich set of operators `==, != , >, <`
  - compare on strings
- numeric comparison:
  - `-eq`, `-ge`, `-ne` ...

#### `(( expr ))`: bash arithmetic conditional

- evaluated as arithmetic expression

## function

```sh
# funciton in subshell, does not affect current shell
function myfunc (
  ...
)

# current shell, function affect your current shell
function myfunc {
  ...
}

# same to above
myfunc () {
  ...
}

# call myfunc
myfunc
```

## Regex

- POSIX BRE/POSIX ERE
  - `egrep` or `-E` to use extended version
  - `grep` by default filter out that don't match

### Special characters

- `.`: any single char
- `|`: OR between regexes
- `\`: special expression
- `()`: enclose expression as subexpression
  - `(hello|goodbye) (Cat|dog)` 

### Quantifiers

- `?`: <=1
- `*`: >=0
- `+`: >=1
- `{n}`: n
- `{n,}`: >=n
- `{,m}`: <=m
- `{n, m}`: between m, n inclusive

### Brackets

- `[]`: a set to match for one char
  - `[abc]`: one of a, b, c

- inside:
  - `-`: range
  - `^`: not in set
  - Named classes: `[[:alnum:]]`
    - `[:alnum:]`: alphanumeric char
    - `[:alpha:]`: alphabetic char
    - `[:blank:]`: space and tab

### Anchors

- `^`: beginning of line
- `$`: end of line

### Backreferences

- Match previous `()` subexpression
- `\n` match nth subexpression
  - e.g. `(123)testing\1` matches `123testing123`
  - exact the same thing


