---
layout: post
title: Useful Unix Command
categories: [Unix, Utils, Wiki]
description: Useful Unix Command
keywords: Unix, Utils, Wiki
---
## Parameter Expansion

- https://wiki.bash-hackers.org/syntax/pe

## Expansions and substitutions

- https://wiki.bash-hackers.org/syntax/expansion/intro

## Compound commands

- https://wiki.bash-hackers.org/syntax/ccmd/intro

## `tr <string1> <string2>`

- translate characters: copies standard input to standard output with substitution or deletion of selected characters

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