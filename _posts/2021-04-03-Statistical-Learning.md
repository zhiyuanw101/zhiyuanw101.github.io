---
layout: post
title: Statistical Learning
categories: [Wiki, Data, Machine Learning, Stats]
description: Information Retrieval
keywords: Wiki, Data, Machine Learning, Stats
---

## Generative Models

### Taxonomy

- Links:
  - https://www.cs.cornell.edu/courses/cs4780/2018fa/lectures/lecturenote04.html
  - https://www.cs.cmu.edu/~tom/mlbook/Joint_MLE_MAP.pdf

- (Probability) Estimation: estimating the **parameters** of a distribution
  - MLE
  - MAP
- Prior probability
  - [probability distribution](https://en.wikipedia.org/wiki/Probability_distribution) that would express one's beliefs about this quantity before some evidence is taken into account
- Posterior probability
  - [conditional probability](https://en.wikipedia.org/wiki/Conditional_probability) that is assigned after the relevant [evidence](https://en.wikipedia.org/wiki/Scientific_evidence) or background is taken into account

### MLE (Maximum Likelihood Estimation)

- Idea
  - $\hat{\theta} = \arg max_{\theta}f_n(x\vert  \theta) $

- Likelihood: 
  - $L_n(\theta) = f_n(x\vert  \theta)$
  - measures the [goodness of fit](https://en.wikipedia.org/wiki/Goodness_of_fit) of a [statistical model](https://en.wikipedia.org/wiki/Statistical_model) to a [sample of data](https://en.wikipedia.org/wiki/Sample_(statistics)) for given values of the unknown [parameters](https://en.wikipedia.org/wiki/Statistical_parameter)
  - similar to probability, formed from the [joint probability distribution](https://en.wikipedia.org/wiki/Joint_probability_distribution) of the sample, but viewed and used as a function of the parameters only. 
- Goal: 
  - find parameters that maximize likelihood function
  - select parameters that gives observed data largest probability
  - get probability distribution based on the parameters

### MAP (Maximum a Posteriori Estimation)

- Idea
  - assume that a [prior distribution](https://en.wikipedia.org/wiki/Prior_distribution) $g$ over $\theta$ exists, treat $\theta$ as a random variable
  - calculate posterior distribution of $\theta$ using Bayes' theorem
  - maximize the posterior $\hat{\theta} = \arg max_{\theta}f(\theta\vert  x) $

- Posteriori
  - posterior probability of $\theta$: $f(\theta \vert  x) = \frac{f(x\vert \theta) \cdot g(\theta)}{f(x)}$
  -  $\hat{\theta} = \arg max_{\theta}f(\theta\vert  x)  = \arg max_\theta f(x\vert \theta)\cdot g(\theta)$

### Naive Bayes Classifier

- Method:
  - Learn prior $P(Y)$ and likelihood $P(X_1, .., X_n\vert Y)$  to calculate $P(Y\vert X_1, ..., X_n)$
  - Choose class to maximize posterior $\arg max_{Y} P(Y\vert X_1, ..., X_n)$

