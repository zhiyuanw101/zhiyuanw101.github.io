---
layout: post
title: Hash index
categories: [DBMS, Wiki]
description: Hash index
keywords: DBMS
---

## Extendible Hashing

- **Elements**
  - Directory: an array of pointers to buckets
  - Data pages: bucket for data entries
  - Global depth: #bits of $h(k)$
  - Local depth: #bits of bucket
    - GD >= LD

- **Insert**
  - Search bucket using hash function
  - If bucket full, split, re-distribute
  - If necessary, double directory
    - When LD = GD

- **Delete**
  - Search bucket using hash function
  - Sibling bucket can be collapsed to one
    - Sibling bucket: Hash key match except for one MSB
    - Remove doubled buckets
    - Collapes split buckets (directory)

- **Features**
  - `#disk access = (directory in mem) ? 1:2`
  - Directory can grow large
    - Doubling directory eveytime when overflow
  - Could have overflow pages

## Linear Hashing

- **Elements**
  - Still have data pages and directory
  - **Level**: $l$ init to 0
  - **Next** (split pointer): $s$ pointer to bucket to be split
  - **Hash** function:
    - $h_{l}$: modulo $N\cdot 2^{l}$
    - $h_{l+1}$: modulo $N\cdot 2^{l+1}$

  - \# bucket:
    - $N$: initial number of buckets
    - $N_{l} = N\cdot 2^{l}$

- **Search**
  - $a = h_l(k)$
  - If $a<s$ use $a = h_{l+1}(k)$: splitted bucket
- **Insert**
  - Search to find bucket
  - If bucket full:
    - add overflow page, insert
      - if bucket is $s$, split first
    - Split $s$ bucket, $s = s+1$
      - If $s = N_l-1$ and split triggered
        - Split the bucket $s$
        - $s = 0$
        - $l = l+1$
  