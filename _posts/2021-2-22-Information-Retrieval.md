---
layout: post
title: Information Retrieval
categories: [Wiki, Data]
description: Information Retrieval
keywords: Wiki, Data
---

## 0. Text Processing

- Token: sequence of char, in particular doc, particular position
- Type: class of all tokens that contain **same** character sequence
- Term: **(normalized)** type included in IR dictionary

### Tokenization

- Analyze text into sequence of discrete tokens
- Important: use same tokenization rules for queries and documents

#### Language Dependent

- Word Segmentation (Chinese Tokenization)
  - Greedy approach: find longest word in dictionary works well

### Normalization

- reducing multiple tokens to same canonical term
- matches despite superficial differences

#### Remove stop words

- High freq words: a, the, in, to (function); I he, she, it (pronouns)
- language dependent

#### Lemmatization

- Reduce inflectional/ variant forms to base form

#### Stemming

- Reduce to 'root' form to recognize morphological variation
- decrease vocab size
- Errors:
  - commission
  - omission
- Performance:
  - improve recall
  - Hurts precision

### Language Identification

- Simplest approach: calculate likelihood of each candidate language, based on training data

#### Approach

- Given sequence $w_1^n$
- For each language, calculate probability: $P(w_1, w_2, ..., w_n)$
  - Approximation:
    - Unigram: $P(w_1, w_2, ..., w_n)=P(w_1)\cdot P(w_2)\cdot ... \cdot P(w_n)$
    - Bigram: $P(w_1, w_2, ..., w_n)=P(w_1)\cdot P(w_2|w_1)\cdot ... \cdot P(w_n|w_{n-1})$
    - N-gram
  - Conditional Probability:
    - $P(w_k|w_{k-1}) = \frac{C(w_{k-1}w_k)}{C(w_{k-1})}$
    - $C()$: Count
  - Smoothing (Avoid zero counts):
    - $P(w_k|w_{k-1}) = \frac{C(w_{k-1}w_k) + 1}{C(w_{k-1}) + V}$
    - $V:$ size of vocab
- Choose language to maximize $P$

#### Start

- $P(w_1) = \frac{C(w_1) + 1}{\text{length} + V}$

- $P(w_1 | <\text{start}>) = \frac{C(w_1) + 1}{C(<\text{start}>) + V}$
- $P(w_1 | <\text{start}>) = \frac{C(<\text{start}>w_1) + 1}{C(<\text{start}>) + V}$

## 1. Text Properties

### Zipf's Law

$$
f\cdot r = k \text{  (for constant $k$)}
$$

- $r$ is rank of word (in sorted list of words by decreasing freq), assume last if tie
- $f$ is word frequency

#### Probability of word

$$
p_r = \frac{f}{N} = \frac{A}{r} \text{  (for constant $A$)}
$$

#### Word freq -> Num of words

- word appearing exactly $f$ times has rank $r_f = \frac{AN}{f}$
- Num of words appearing exactly $f$ times: $I_f = r_f-r_{f+1} = \frac{AN}{f(f+1)}$

#### Word freq -> Fraction of words 

- rank of occuring once (vocab size): $V = \frac{AN}{1}$
- Fraction of words with freq $f$: $\frac{I_f}{V} = \frac{1}{f(f+1)}$

#### Usage

- Distribution of terms in corpus

### Heap's Law

$$
V=KN^{\beta} \text{  (with constants $K, 0<\beta <1$)}
$$

- $V$: vocab size
- $N$: corpus size
- Typical constant: $K=10-100, \beta=0.4-0.6$

#### Usage

- estimate vocab size by corpus size

## 2. Boolean Retrieval

