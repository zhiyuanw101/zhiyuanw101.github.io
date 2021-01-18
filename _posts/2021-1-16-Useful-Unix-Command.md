---
layout: post
title: Useful Unix Command
categories: [Unix, Utils, Wiki]
description: Useful Unix Command
keywords: Unix, Utils, Wiki
---

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

- Display, set or unset values of shell attributes and positional parameters