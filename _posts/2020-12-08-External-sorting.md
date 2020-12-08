---
layout: post
title: External sorting
categories: [DBMS, Wiki]
description: sorting in DBMS
keywords: DBMS
---

- Problem:
  - sort 1 TB data, not able to fit in memory
  - minimize disk access cost
  - suppose $N$ pages to be sort

## Two-Way External Merge Sort

- use 3 **buffer pages**
  - 2 input buffer
  - 1 output buffer
- pass 0: read, sort each page, create **run** (sorted sequence)
  - $N$ runs
  - each run 1 page
- pass 1+: load 2 pages, merge, write pages back
- cost:
  - \# of passes: $1+\lceil\log_2N\rceil$
  - \# page I/Os: $2N(1+\lceil\log_2N\rceil)$
    - read, write each page every pass

## General External Merge Sort

- use $B$ buffer pages
  - $B-1$ input buffers
  - 1 output buffers
- pass 0: use $B$ buffer pages sort them internally
  - $\lceil N/B \rceil$ sorted **runs**
  - each **run** $B$ pages long
- pass 1+: merge $(B-1)$ runs using $B-1$ buffers
  - load first (sorted) page of each run to input buffers, load next once empty
  - pick smallest, move to output buffer, flush output once full
- cost:
  - \# of passes: $1+\lceil\log_{B-1}\lceil N/B\rceil \rceil$
  - \# page I/Os: $2N(1+\lceil\log_{B-1}\lceil N/B\rceil \rceil)$

## Replacement Sort

- features
  - only in pass 0
  - creat longer run:
    - $M = (B-2)$
    - average $2M = 2(B-2)$ pages each run
  - reduce \# passes
- use $B$ buffers:
  - 1 **input buffer**
  - $B-2$ **current set**
  - 1 **output buffer**

- process:
  - start:
    - read pages from **file** to **current set**
    - read page from **file** to **input buffer**

  - repeat:
    - pick smallest value from current set that is greater than largest value in output buffer
      - write to output buffer, if output buffer full, flush output
      - read from input buffer, if input buffer empty, read input buffer
      - if such value does not exist, flush output, start new run

- cost:
  - \# passes: $1+\lceil\log_{B-1}\lceil \frac{N}{2(B-2)}\rceil \rceil$

## Blocked I/Os & Double buffering

- Blocked I/Os
  - $B/b$ buffers
    - $b$ block size
  - features:
    - reduce cost per I/O (sequential access to disk)
    - increase \# pass (2-3)

- Double buffering
  - $B = 2(K+1)b$ main memory buffers
  - features:
    - prefetch into shadow block
    - increase \# pass (2-3)
- cost:
  - change buffer parameter $(B-1) => \lfloor(B/b)\rfloor -1$

## B+ Tree Sort
B+ tree index on sorting colunm(s)
- Clustered:
  - go to left-most leaf, retrieve all leaf pages
  - always better than external sort
- Unclustered:
  - cost:
    - $pN$
    - $p$ avg \# of records per page
    - one I/O each record
  - usually worse than external sort, for extremely selective queries