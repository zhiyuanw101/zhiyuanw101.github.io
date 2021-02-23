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
    - Bigram: $P(w_1, w_2, ..., w_n)=P(w_1)\cdot P(w_2\vert w_1)\cdot ... \cdot P(w_n\vert w_{n-1})$
    - N-gram
  - Conditional Probability:
    - $P(w_k\vert w_{k-1}) = \frac{C(w_{k-1}w_k)}{C(w_{k-1})}$
    - $C()$: Count
  - Smoothing (Avoid zero counts):
    - $P(w_k\vert w_{k-1}) = \frac{C(w_{k-1}w_k) + 1}{C(w_{k-1}) + V}$
    - $V:$ size of vocab
- Choose language to maximize $P$

#### Start

- $P(w_1) = \frac{C(w_1) + 1}{\text{length} + V}$

- $P(w_1 \vert  <\text{start}>) = \frac{C(w_1) + 1}{C(<\text{start}>) + V}$
- $P(w_1 \vert  <\text{start}>) = \frac{C(<\text{start}>w_1) + 1}{C(<\text{start}>) + V}$

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

### Term-document incidence matrix

- 1 if term in the document, 0 otherwise
- construct query as boolean form

### Inverted Index

- map each term to posting list of documents containing it
  - Doc -> docID
  - Dictionary of terms
- Creating Inverted Index:
  1. assemble all <term, docID> pairs
  2. sort by term, then by docID
  3. Merge, split into dictionary + posting list, add document frequency information
- Query Processing
  - AND
  - OR
  - Best order: in order of increasing term freq
    - consider worse case of OR: add up two OR
    - start with smallest set

### Extension: Phrase Queries

#### Solution1: Biword Indexes (Phrase Indexes)

- index bigram in as vocabulary term
- longer phrase: break into conjunction of biword
- Drawbacks:
  - false positives: accross different sentences
  - larger dictionary

#### Solution2: Positional Indexes

- Posting list:
  - for each token, document:
    - store position in which token appears in document
- Merge algorithm:
  - Posting list level: matching docID
  - Document level: match consecutive positions for query tokens
- Drawbacks:
  - expand storage substantially: 2-4 times larger

#### Combined Strategy

- Use phrase indexes (biword indexes) for:
  - phrase known to be common based on recent querying behavior
  - individual words are common, desied phrase is rare
- Use Positional Indexes for remaining

### Boolean Retrieval vs. Ranked Retrieval

- hard to tune precision vs. recall:
  - AND: high precision, low recall
  - OR: low precision, high recall
- Hard to rank



## 3. Ranked Retrieval

- **ranked retrieval** normally associated with **free text queries**
- need way to assign **score** to query/ document pair

### Approach 1: Jaccard coefficient

$$
\text{Jaccard}(A, B) = \frac{\vert A \cap B\vert }{\vert A \cup B\vert }
$$

- measure of overlap of two **sets** $A, B$

- Issues:
  - does not consider **term frequency**
  - does not consider rare terms over frequent terms

### Approach 2: Vector-Space Model

- term-document matrix

  - Unique "orthogonal" terms, form vector space, dimension = \vert vocab\vert 
  - Document & query represent as t-dimensional vectors
  - entry in matrix: **weight** of term in document

- term frequency $tf_{t, d}$

  - number of times $t$ occurs in $d$
  - Normalize: $tf_{t, d} = f_{t, d}/max(f_{t, d})$

- inverse document frequency $idf_t$

  - Motivation: 

    - term freq not enough: relevance should not increase proportionally with $tf$
    - **rare words** more informative, want higher weights for rare terms in collection
    - **frequent words** in collection still have high weights

  - $$
    idf_t = \log_{10}{\frac{N}{df_t}}
    $$

  - $df_t$ document frequency for term $t$: number of documents that contains $t$

  - $N$ total number of documents in collection, much larger than $df_t$

  - collection frequency: number of occurence of $t$, counting multiple occurrence

- tf-idf weighting
  $$
  \text{W}_{t, d} = \text{tf}_{t, d} \cdot \text{idf}_t = \text{tf}_{t, d} \cdot \log_{10}{\frac{N}{\text{df}_t}}
  $$

  - **increase** with **number of occurences** within document
  - **increase** with **rarity** of term in collection

### Similarity Measure

- Euclidean distance
  - issue of normalization
- Manhattan distance
  - issue of normalization
- Inner Product
  - issue of normalization
  - measure how many terms matched but not how many not matched??
- Cosine Similarity√√

### Issues

- missing semantic info (e.g. word sense)
- missing syntatic info (e.g. phrase structure, term order)
- assumption of term independence

## 4. Metrics

### Precision

$$
\text{Precision} = \frac{\# \text{relevant retrieved}}{\# \text{total retrieved}} = \frac{tp}{tp + fp}
$$



### Recall

$$
\text{Recall} = \frac{\# \text{relevant retrieved}}{\# \text{total relevant}} = \frac{tp}{tp + fn}
$$

### Marco

- average

### Micro

- Sum of numerator / sum of denominators

### TopN

- Precision: use TopN as retrieved for denominator
- Recall: use all as relevant for denominator

## 5. Alternative IR Model

### Probability Model

- Probability Ranking Principle
  - calculate $P(\text{rel} \vert  D_i)$
  - rank documents on decreasing probability of relevance to user
- Combination of relevance and non-relevance

- F4 Reweighting 

### Latent Semantic Analysis / Indexing

Reference: [stanford](https://nlp.stanford.edu/IR-book/html/htmledition/latent-semantic-indexing-1.html)

- Motivation:
  - Synonymy: various word, same concept should handled together
  - Independence: two terms frequently together 
- Objective:
  - learn vectors that is
    - short
    - dense
  - replace term indexes with concepts
- Approach:
  - SVD: Map term vector space to lower dimensional space.
- **SVD**:
  - $X=T_0S_0D_0$
    - $S_0$ is <u>diagonal matrix</u> of <u>singular values</u>
    - $T_0, D_0$ left and right <u>singular vectors</u>
  - Reduce $S_0$, delete lower rows and columns
    - keep 300 ~ 500 latent concepts
    - $X' = TSD$

### Fuzzy Set Model

- *fuzzy* framework:
  - Each **term** associated with a *fuzzy* set
  - Each **doc** has a degree of membership in fuzzy set
- Thesaurus: $C$ is term-term correlation matrix 
  - $C(i, j) = \frac{n(i, j)}{n(i) + n(j) - n(i, j)}$, for $K_i, K_j$
    - $n(i)$ Is number of documents contains $K_i$
    - $n(i, j)$ is number of documents contains both $K_i, K_j$
  - Notion of proximity between terms
- Define: $K_i$ fuzzy set membership for document $D_j$:
  - $\mu(K_i, D_j) = 1-\prod_{K_l \in D_j}(1-C(i, l))$
  - membership of $D_j$ in fuzzy set associated with $K_i$
  - $\mu(\neg K_i, D_j) = 1- \mu(K_i, D_j)$
- Disjunctions and Conjunctions
  - Disjunctive set: $\mu(K_1\vert  K_2 \vert  ... \vert K_n, D_j) = 1-\prod(1-\mu(K_i, D_j))$
  - Conjunctive set: $\mu(K_1 \wedge K_2 \wedge ... K_n, D_j) = \prod (\mu (K_i, D_j))$

## 6. Word Representations

### A. Sparse representations

#### Vector Space Model

- just use term vector

#### Mutual-information co-orrurrence matrices

- **Positive Pointwise Mutual Information** (PPMI)
  - Pointwise mutual information: 
    - Does $X, Y$ co-occur more than if they were independent
    - co-occur could be entire document
    - $\text{PMI}(X, Y) = \frac{P(X, Y)}{P(X)\cdot P(Y)}$
  - words PMI
    - $\text{PMI}(word1, word2) = \frac{P(word1, word2)}{P(word1)\cdot P(word2)}$
  - PPMI: 
    - replace negative (unrelatedness) with 0
    - $\text{PPMI}(word1, word2) = \max{(\frac{P(word1, word2)}{P(word1)\cdot P(word2)}, 0)}$
- **Word-word or Word-context matrices**
  - **context**: use smaller context instead of entire document
    - paragraph
    - **window** 
    - size of window depend on goal:
      - Syntatic: 1-3
      - Semantic: 4-10
  - idea: similar meaning if similar context (vector)
  - **matrix**:  $\vert V\vert \times\vert V\vert $, each vector length $\vert V\vert $
  - **PPMI** on Term-Context Matrix
    - PMI is biased towards infrequent events
      - Laplace smoothing: add 2 to count before computing PPMI

#### Explicit Semantic Analysis

- Idea:
  - use document corpus as knowledge base
  - in ESA, a word is represented as a column vector in the [tf–idf](https://en.wikipedia.org/wiki/Tf*idf) matrix of the text corpus and a document (string of words) is represented as the [centroid](https://en.wikipedia.org/wiki/Centroid) of the vectors representing its words.
  - Typically, the text corpus is [English Wikipedia](https://en.wikipedia.org/wiki/English_Wikipedia)

### B. Dense vector representations

#### Singular Value Decomposition (SVD)

- SVD applied to PPMI Word-Word matrix
- $X = T_0S_0D_0$ 
  - $T_0,S_0,D_0\in \vert V\vert \times \vert V\vert $ 
- Reduced to $X=TSD$
  - use rows of $T\in \vert V\vert \times k$ 

#### Neural network models 

- Idea: 
  - Learn embeddings as part of process of word prediction
  - Train NN to predict context
- Models:
  - Word2vec
    - Skip-gram: predict context given word
    - CBOW: predict word given context
  - transformer (bert)
    - Self-attention
    - Multi-head
- Training: (word2vec)
  - negative samples: random context
  - Loss: 
    - minimize distance in positive example
    - maximize distance in negative example







