---
layout: post
title: 自然语言处理 Neural Language Processing [Neural Network Methods for Natural Language Porcessing 阅读笔记]
categories: [Algorithms, NLP, Readings, Wiki]
description: 文献：Neural Network Methods for Natural Language Porcessing*, Yoav Goldberg, 2018
keywords: Algorithms, NLP, Readings, Notes
---
## 1. Intro

### Deep Learning Approach in NLP

#### Feed-forward networks[multi-layer perceptrons (MLPs)]

- 可以忽次序的输入(一般固定大小)
- 替换线性模型(Linear Model)

#### Networks with convolutional and pooling layers

- 提供较强Local pattern信息，忽略相对位置

#### Recurrent and recursive architectures

- 处理任意大小的结构化数据， 如：树，序列(tree, sequence)
- Recurrent networks: 序列建模
- Recursive networks: Recurrent networks的推A广，树建模
- 允许对 *Markow Assumption* 的放弃

---

## 2. Learning Basics and Linear Models

### 2.1 Linear functions

- *hypothesis classes* are linear functions or decision trees
- Take the form $f(\textbf{x}) = \textbf{W}\cdot \textbf{x}+\textbf{b}$
- parameters $\textbf{W}, \textbf{x}$ refered to as $\theta$
- Con: restricted to linear functions
- Pros:
  - efficient to train
  - interpretable

### 2.2 Train, test, validation set

- Leave-one out
- Held-out set:
  - 80/20 split
- Three-way splic:
  - divide into *train, validation(development), test set*
  - experiments, tweaks, error analysis, selection on *validation set*
  - single run of final model over *test set*

### 2.3 Linear models

- **Linear separable**: can be separated by straight line

#### Binary classification

$$\hat{y} = \text{sign}(f(\textbf{x})) = \text{sign}(\textbf{w}^T\cdot \textbf{x}+\textbf{b})$$

- Log-Linear:

$$\hat{y} = \sigma(f(\textbf{x}))= \frac{1}{1+e^{-(\textbf{w}^T\cdot \textbf{x}+\textbf{b})}}$$

### 2.4 Multi-class classification

$$\hat{\textbf{y}} = \textbf{W}\cdot \textbf{x}+\textbf{b}$$

- Log-Linear:
  - 可以解释为概率分布(probability distribution)

$$\hat{\textbf{y}} = \text{softmax}(\textbf{W}\cdot \textbf{x}+\textbf{b})$$

### 2.5 Representation

- $\hat{\textbf{y}}$
- $\textbf{x}$
- rows of $\textbf{W}$: usually word representation
- columns of $\textbf{W}$
- Linear models: representations are interpretable

### 2.6 Training as Optimization

#### Loss Function:

$$L(\theta) = \frac{1}{n}\sum_{i=1}^n{L(\hat{\textbf{y}}, \textbf{y})}$$

- Function that map 2 vectors to a scalar
- Hinge loss:
  - Margin loss/ SVM loss
  - used in linear outputs, not model with probability
- Log loss: soft version of Hinge
- Cross-entrophy:
  - common in log-linear models and neural nets
  - assumed using softmax
- Ranking loss:
  - defined for pair of correct and incorrect examples

#### Regularization

Score complexity

- $L_2$ Regularization
  - prefer to decrease value >1
- $L_1$ Regularization
  - decrease all non-zero, sparse solution
- Elastic-Net
  - Combination of $L_1, L_2$
- Dropout

### 2.7 Gradient based Optimization

SGD:

```bash
while
    Sample x_i, y_i
    Compute loss L(f(x_i, a), y_i)
    Compute gradient G of L w.r.t parameters a
    a = a - tG
return a
```

*minibatch* SGD:

- sample $m$ samples every iteration

---

## 3. Linear Model to Multi-layer Perceptrons

motivation: XOR, not linearly separable

### 3.2 Nolinear input transformation

$$\hat{\textbf{y}} = f(\textbf{x}) = \phi(\textbf{x})\textbf{W}+\textbf{b}$$

- define a function $\phi$ to map the input to a representation that is linearly separable
- often map to higher dimension

### 3.3 Kernal Methods

- Kernalized Support Vector Machines(SVMs):
  - define set of generic mappings, map to very high dimentional, even infinite spaces
  - example: *polynomial mapping*
  - Pros: *kernal tricks*, work in transformed space without computing transformed representation
  - Cons: high dimentional: overfitting,

---

## 4. Feed-forward Neural Networks

### 4.2 Mathematical Representation

- $\text{MLP}2$ :

$$
\textbf{h}^1 = g^1(\textbf{x} \textbf{W}^1+\textbf{b}^1)\\
\textbf{h}^2 = g^2(\textbf{h}^1 \textbf{W}^1+\textbf{b}^1)\\
\text{NN}_{\text{MLP2}}(\textbf{x}) = \textbf{y} = \textbf{h}^2\textbf{W}^3+\textbf{b}^3\\
$$

- *fully-connected* (*affine*): layers resulting from linear transformation

### 4.3 Representation Power

- MLP1 is universal approximator, but may be hard to train

### 4.4 Common Nonlinearities

- Sigmoid
- tanh
- Hard tanh
  - approximation of tanh, faster to compute derivatives
- ReLU
  - often combined with dropout regularization

### 4.5 Regularization and Dropouts

- $L_2$ (weight decay) effective for neural networks
- dropouts:
  - prevent networks from learning to rely on specific weights
  - training:
    - randomly drop $1-p$ (usually 0.5) of the net in one stage
    - reinserted into the network with original weights
    - more epoch, faster each epoch, improve training speed
  - testing:
    - approximation by using the full network with each node's output weighted by $p$
    - expected value of output of any node is same as training stage

### 4.7 Similarity and Distance Layers

- Dot Product
- Euclidean Distance
- Trainable Forms:
  - bilinear form: $\text{sim}(\textbf{u}, \textbf{v}) = \textbf{u}\textbf{M}\textbf{v}$
  - trainable distance function: $\text{dist}(\textbf{u}, \textbf{v}) = (\textbf{u}-\textbf{v})\textbf{M}(\textbf{u}-\textbf{v})$
  - MLP with single output, input concatenation of vectors

### 4.8 Embedding Layers

- input distinct **symbolic categorical features** (word)
- parameters in symbolic layer: $\textbf{E}\in R^{|vocab|\times d}$, each **row** corresponds to **different word** in vocabulary
- lookup: indexing $v_i = \textbf{E}_{[i, :]}$, if input one-hot: $\textbf{x}\textbf{E}$

---

## 5. Neural Network Training

### 5.1 Computation Graph Representation

- Definition: Representation of an arbitrary mathematical computation as a graph
- directed acyclic graph (DAG):
  - **nodes** are mathematical operations or variable
  - **edges** are flow of intermediary values between nodes.

#### backward computation(backprop)

- let node $N$ node with be scalar output (loss-node), $\forall i \in \{1,2,... , N\}$, we compute $d(i) = \frac{\partial N}{\partial i}$. The backprop fills table of values $d(1), d(2), ..., d(N)$
- node  $i$ method:
  - forward: $f_i$, $v(i) = f_i(v(a_1), ...v(a_m)),\pi^{-1}(i) = \{a_1, ... a_m\}$
  - backward: $\frac{\partial f_i}{\partial x}, \forall x \in \pi^{-1}(i)$
  - notation:
    - $f_i$ is the operation at node $i$
    - $v(i)$ is output of node $i$
    - $\pi^{-1}(i)$ is set of children node of $i$
    - $\pi(i)$ is set of parent node of $i$
- algorithms:

```cpp
d(N) = 1
for i = N-1 to 1 do:
    d(i) = 0
    for j in parents of i:
        d(i) += d(j) * (partial(f_j)/partial(i))
```

- note: gradient $\frac{\partial f_i}{\partial x}$:
  - think in terms of contribution to computation
  - $\text{max}(0, x)$ gradient: $1$ for $x>0$, $0$ otherwise
  - $pick(\textbf{x}, 5)$ gradient is vector $\textbf{g}, \textbf{g}_{[5]} = 1, \textbf{g}_{[i \neq 5]} = 0$

#### Dynamic and Static graph in software implementation

- Static Graph: Tensorflow
  - graph shape defined at the beginning
  - use place-holder for input/output
  - compiler to optimize graph
- Dynamic graph:
  - different graph is created for each training sample

#### Implementation Recipe

```cpp
Define parameters
for iteration = 1 to T do
    for Training sample x_i, y_i do
        loss_node = build_computation_graph(x_i, y_i, parameters)
        loss_node.forward()
        gradients = loss_node.backward()
        parameters = update_parameters(gradients, parameters)
return parameters
```

### 5.2 Practicalities

#### Initialization

- *xavier initialization*: tanh
- zero-mean Gaussian distribution with $\text{stddev} = \sqrt{\frac{2}{d_{in}}}$: ReLU

#### Vanishing and Exploding Gradients

- vanishing gradients:
  - exceedingly close to 0
  - step-wise training
  - batch-norm
  - use specialized architecture for gradient flow (LSTM, GRU)
- exploding gradients:
  - clipping

---

## 6. Features for Textual data

- *feature extraction/feature representation*: mapping from textual data to vectors, done by *feature function*

### 6.1 Typology of NLP Classification Problems

- Word (Token):
  - word: meaning-bearing unit
  - token: output of tokenization, split based on whitespace and punctuation
- Text: phrase/sentence/ paragraph/ document
- Paired Texts: pair of words or longer texts
- Word in Context
- Relation between words

### 6.2 Features for NLP Problems

- *indicator feature*: 0/1
- *count*: number of times occured

#### Directly Observable Properties

##### Single words:

- *Lemmas* and *Stems*:
  - Lemma: dictionary entry of word, (booking, booked, books --> book)
  - Stems: coarser than lemmatization, work on any sequence of letters(miss-spelled), result may not be word. (picturing, pictured --> pictur)
- *Lexical Recources*:
  - essentially dictionary accessed by machines
  - information for word, linking to other words
  - words belong to *synsets*, describe cognitive concept, linked by hypernymy/ hyponymy/ antonyms/ holonyms/ meronyms
- Distributional Information

##### Features for Text

- Bag of Words (BOW):
  - each word count as feature
- Weighting:
  - external statistics
  - TF-IDF weighting, when using BOW

##### Features of Words in Contexts

- Windows:
  - versionof BOW, restricted within window
  - biRNN architecture, trainable window
- Position

##### Features for Word Relations

- *Distance*
- *Identities* of words between

#### Inferred Linguistic Properties

- **part of speech (POS)**
  - syntatic chunk
  - local information
  - NOUN, PREP, DET, ADJ, VERB/ NP, PP, VP
- **constituency tree/ phrase-structure tree**
  - global syntactic structure
  - grouping of words into phrases
  - nested, hierarchy of syntactic units
  - NP, PP, VP
- **dependency tree**
  - syntactic relations
  - modification relations/ connections (modifiers of verb)
- **semantic role labeling**
  - semantic relations
- *discourse relations*
  - connect sentence together
  - ELABORATION, CONTRADICTION, CAUSEEFFECT
- *anaphora*

#### Core Features VS. Combination Features

Neural networks provide nonlinear models, solve combination

#### Ngram Features

- *ngrams*: consecutive word sequence of a given length
- vanilla neural networks cannot infer *ngrams* features
- MLP with windows and position information can infer *ngrams* features
- CNNs, BiRNNs better

#### Distributional Features

- distributional hypothesis: meaning of word can be inferred from contexts.
- *clustering-based methods*: assign to similar words same cluster and represent each word by cluster
- *embedding-based methods*: represent words as vectors, similar words result in closer vectors

---

## 7. Case Studies: NLP Features

### 7.4 Part of Speech Tagging (POS)

- *POS Tag*: assign correct part-of-speech to each word in sentence
- structured task
- intrinsic cues, extrinsic cues

### 7.5 Named Entity Recognition (NER)

- *NER*: find named entities in document, task can be context dependent
- sequence segmentation task, performed using *BIO encoded tags*

### 7.6 Preposition Sense Disambiguation

- prepositions: on, in, with, for
- approach: use heuristic + POS-tagger
- approach: use denpendency parser

### 7.7 Denpendency Parsing

- denpendency parsing: return syntatic dependency tree over a sentence
- approach: arc-factored approach

---

## 8. From Textual Features to Inputs

### 8.1 Encoding Categorical Features

#### one-hot

- each dimension correspond to a unique feature instance, 0/1

#### dense encoding (feature embeddings)

- general structure for NLP classification system:
    1. extract set of *core* linguistic features $f_1,...f_k$
    2. for feature $f_i$, retrieve embedding vector $v(f_i)$
    3. combine embedding vectors (summation/concatenation/both) into input vector $\textbf{x}$
    4. feed $\textbf{x}$ into nonlinear classifier and train
- only need to define structure of embedding vector, is treated as network parameters and trained

#### relation between one-hot and dense vector

- first layer serve as embedding layer when fed in one-hot input

### 8.2 Combining Dense Vectors

#### Window-based features

- concatenation:
  - $[\textbf{a};\textbf{b};\textbf{c};\textbf{d}]$
  - care about relative position
- summation:
  - $\frac{1}{2}\textbf{a}+\textbf{b}+\textbf{c}+\frac{1}{2}\textbf{d}$ 
  - don't care order
  - could assign weights
- Note on notation:
  - $([\textbf{x};\textbf{y};\textbf{z}]\textbf{W}+\textbf{b})$ is equivalent to 
  - $(\textbf{x}\textbf{U} +\textbf{y}\textbf{W}+ \textbf{z}\textbf{V}+\textbf{b})$

#### Variable Number of Features: CBOW

- continuous bags of words (CBOW): summing or averaging embedding vectors of corresponding features, discard order information
- $\text{CBOW}(f_1, ..., f_k) = \frac{1}{k}\sum_{i = 1}^k{v(f_i)}$
- could use TF-IDF score to assign weights

### 8.4 Odds and Ends

#### distance

- in practice, bin distances into several groups  (1, 2, 3, 4, 5-10, 10+)
- distance embedding: each bin associated with d-dimentional vector, trained as regular parameters

#### Padding, Unknown, Word Dropout

- padding: add padding symbol into embedding vocabulary
- *out-of-vocabulary*(OOV): special symbol *UNK*
- Dropouts:
  - model needs to be exposed to unknown-word condition during training
  - when extracting features in training, randomly replace words with unknown symbol
  - could serve as regularization

#### Network Output

- for multi-class classification, $k$-dimensional vector output
- $d\times k$ matrix in output layer
- columns of the matrix thought as $d$-dimensional  embeddings of output class

### 8.5 Example: POS Tagging

### 8.6 Example: Dependency

---

## 9. Language Modeling

### 9.1 Language Modeling Task

- Language Modeling:
  - assign probability to any sequence of words $p(w_{1:k}) = p(w_1, ..., w_k)$
  - assign probability for a word following sequence of words$p(w_i\vert w_{1: i-1})=p(w_i\vert w_1, .., w_{i-1})$
  - equivalent:
    $$
    p(w_{1:k}) = p(w_1)p(w_2|w_1)p(w_3|w_{1:2})...p(w_k|w_{1:k-1})\\
    p(w_i|w_{1:i-1}) = \frac{p(w_{1:i})}{p(w_{1:i-1})}
    $$
- *markow-assumption*:
  - $k$th order markov-assumption: only depend on last $k$ words
  - $p(w_{i}\vert w_{1:i-1}) = p(w_i\vert w_{i-k+1:i})$

### 9.2 Evaluating Language Models: Perplexity

- how well a probability model predicts a sample
- lower perplexity better fit
- corpus specific, two model must compare w.r.t. same evaluation corpus
- $2^{-\frac{1}{n}\sum_{i=1}^n{\log_2{\text{LM}(w_i\vert w_{1:i-1})}}}$

### 9.3 Traditional Approaches

- MLE:
  - $$\hat{p}_{\text{MLE}}(w_{i+1} = m|w_{i-k:i}) =\frac{\#(w_{i-k:i+1})}{\#(w_{i-k:i})}$$
  - zero probability: infinite perplexity
- smoothing techniques
- limitations:
  - k-gram, design by hands
  - expersive in terms of memory
  - lack of generalization

### 9.4 Neural Language Models

- Example:
  - input: k-grams of wards $w_{1:k}$, k-context treated as word window $\textbf{x} = [v(w_1); ...; v(w_k)]$
  - output: probability distribution over next word
  - MLP:
    $$
    v(w_i) = \textbf{E}_{[w_i]}\\
    \textbf{x} = [v(w_1); ...; v(w_k)]\\
    \textbf{h} = g(\textbf{x}\textbf{W}^1+\textbf{b}^1)\\
    \hat{\textbf{y}} = p(w_{k+1}|w_{i:k}) = LM(w_{k+1}|w_{i:k}) = \text{softmax}(\textbf{h}\textbf{W}^2+\textbf{b}^2)
    $$
- Memory and Computational Efficiency
  - linear increase in number of parameters w.r.t. $k$
  - softmax and cross-entropy is slow when $V$ is large
- Large output spaces ($V$): methods to accelerate softmax

### 9.5 Using Language Models for Generation

- generating sentences (decoding language model): sample random word, *beam search*

---

## 10. Pre-trained Word Representations

### 10.4 Word Embedding Algorithms

- Two ideas lead to two approaches:
  - Distributional semantics:
    - idea: statistics based, words tend to appear in similar context with similar meaning
    - word-context matrix (co-occurence matrix)
    - SVD based methods
  - Distributed representation:
    - idea: meaning and relations are captured in vectors, distributed in different dimension of vector
    - iteration based
    - word2vec

#### SVD based, Distributional Semantics

- **word-context matrix**: $\textbf{M}\in R^{\vert V_{W}\vert\times \vert V_{C}\vert}$, $\vert V_{W}\vert$ is set of all words,  $\vert V_{C}\vert$ is set of all contexts
- entries in $\textbf{M}$: $\textbf{M}_{[i, j]}^f = f(w_i, c_j)$, $f$ is association measure of strength between a word and a context
- **pointwise mutual information** (PMI): association measure between 2 discrete outcomes:
  - $\text{PMI}(x,y) = \log {\frac{P(x, y)}{p(x)P(y)}}$
  - $f(w,c) = \text{PMI}(w, c) = \log{\frac{num (w, c) \cdot \vert D\vert}{num(w) \cdot num(c)}}$, $\vert D\vert$ is corpus size
  - favor informative contexts for a given words - contexts that co-occur more with given word
  - usually use *positive PMI* (PPMI)
- *dimensionality reduction*: **singular value decomposition** (SVD):
  - $\textbf{M} = \textbf{U}\textbf{D}\textbf{V}$
  - $\textbf{U}\in R^{\vert V_{W}\vert\times \vert V_{W}\vert}$, orthonormal
  - $\textbf{D}\in R^{\vert V_{W}\vert\times \vert V_{C}\vert}$, diagonal
  - $\textbf{V}\in R^{\vert V_{C}\vert\times \vert V_{C}\vert}$, orthonormal
  - only consider first $k$ ranks of $\textbf{D}$, $\textbf{M}' = \textbf{U}'\textbf{D}'\textbf{V}'$ is low rank approximation of $\textbf{M}$
  - $\textbf{E} = \textbf{U}'\textbf{D}'$, distance between rows equivalent to $\textbf{M}'$, use row as word vector
- similarity measures:
  - *cosine similarity*
  - *generalized Jacaard similarity*

#### Iteration based methods, word2vec

##### word2vec

- 2 algorithms:
  - CBOW: predict center words from contexts
  - skip-gram: predict distribution of context words from center word
- 2 training methods:
  - negative sampling
  - hierarchical softmax

###### CBOW

###### skip-gram

###### GloVe (Global Vectors for Word Representation)
