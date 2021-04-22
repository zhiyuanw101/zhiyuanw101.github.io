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
  - EM
- Distribution (Model)
  - Naive Bayes
  - Univariate Gaussian
  - Multivariate Gaussian Distribution
  - Gausian Mixture Model (GMM)
  - Baysian Network
  - Hidden Markov Model (HMM)
- Prior probability
  - [probability distribution](https://en.wikipedia.org/wiki/Probability_distribution) that would express one's beliefs about this quantity before some evidence is taken into account
- Posterior probability
  - [conditional probability](https://en.wikipedia.org/wiki/Conditional_probability) that is assigned after the relevant [evidence](https://en.wikipedia.org/wiki/Scientific_evidence) or background is taken into account

### Parameter Estimation

#### MLE (Maximum Likelihood Estimation)

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

#### MAP (Maximum a Posteriori Estimation)

- Idea
  - assume that a [prior distribution](https://en.wikipedia.org/wiki/Prior_distribution) $g$ over $\theta$ exists, treat $\theta$ as a random variable
  - calculate posterior distribution of $\theta$ using Bayes' theorem
  - maximize the posterior $\hat{\theta} = \arg max_{\theta}f(\theta\vert  x) $

- Posteriori
  - posterior probability of $\theta$: $f(\theta \vert  x) = \frac{f(x\vert \theta) \cdot g(\theta)}{f(x)}$
  -  $\hat{\theta} = \arg max_{\theta}f(\theta\vert  x)  = \arg max_\theta f(x\vert \theta)\cdot g(\theta)$

#### EM (Expectation Maximization)

- Idea
  - Estimate parameters with MLE or MAP when model depends on **unobserved latent variables**.
    - GMM: unobserved cluster labels
- Description:
  - Given: $X$ observed data, unobserved latent variables $Z$, and joint likelihood $L(\theta; X, Z) = p(X, Z \vert \theta)$
  - Maximize marginal likelihood of observed data $L(\theta; X) = p(X\vert \theta) = \sum_Z p(X, Z \vert \theta)$, however equlity is often **intractable**
  - Steps:
    - Expectation step:
    - Maximization step:
- Example: 
  - GMM
    - E-step: fix parameters, softly assign examples to clusters
    - M-step: re-estimate each cluster parameters

### Model (Distribution)

#### Naive Bayes Classifier

- Method:
  - Learn prior $P(Y)$ and likelihood $P(X_1, .., X_n\vert Y)$  to calculate $P(Y\vert X_1, ..., X_n)$
  - Choose class to maximize posterior $\arg max_{Y} P(Y\vert X_1, ..., X_n)$

#### Bayesian Network

- Ideas:
  - Joint probability contains all information: marginal, conditional
    - $P(b) = Σa Σc Σd P(a, b, c, d) $
    - $P(c \vert b) = Σa Σd P(a, c, d \vert b) $
  - Chain rule of Factoring: 
    - $P(a, b, c, … z) = P(a \vert b, c, …. z) P(b \vert c,.. z) P(c\vert .. z)..P(z)$
  - Conditional independence
    - $P(X1, X2,…. XK \vert C) = Π P(Xi \vert C)$
    -  Naïve Bayes assumption
  - Graph graph <==> Conditional independence relations
    - $p(X1, X2,....XN) = Π p(Xi \vert parents(Xi))$

#### Univeriate Gaussian

- i.i.d assumption

  - identical
  - Independent

- Estimation

  - $$
    \mu_{MLE} = \sum_{i=1}^n{\frac{x^{(i)}}{n}}
    $$

  - $$
    \sigma^2_{MLE} = \sum_{i=1}^n{\frac{(x^{(i)}-\mu_{MLE})^2}{n}}
    $$

#### Multivariate Gaussian Distribution

- Characterized by mean vector & covariance matrix

- Spherical Gaussian

  - $$
    \Sigma = \sigma^2\mathbf{I}_d
    $$

  - $$
    \overline{\mu}_{MLE} = \sum_{i=1}^n{\frac{{\overline{x}^{(i)}}}{n}}
    $$

  - $$
    \sigma^2_{MLE} = \sum_{i=1}^n{\frac{\vert\vert\overline{x}^{(i)}-\overline{\mu}_{MLE}\vert\vert^2}{nd}}
    $$

#### Gaussian Mixture Model (GMM)

##### Known Labels

- Likelihood:

$$
P(S_n) =\prod_{i=1}^n\sum_{j=1}^k\delta(j\vert i)\gamma_j N(\overline{x}_{(i)} \vert \overline{\mu}^{(j)}\sigma^2_j)
$$

- $\delta(j\vert i)$ is indicator function
- $\gamma_j$ is probability of cluster $j$
- MLE with log-likelihood

##### Unknown Labels

- EM for GMM



