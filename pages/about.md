---
layout: page
title: About
description: 
keywords: Zhiyuan Wang
comments: true
menu: About
permalink: /about/
---
> Hi! This is Zhiyuan Wang. I am a junior studying Computer Science and Mathematics at the University of Michigan. I love tennis, film, classical music and video games. I want to have a dog.

### Education

---
**University of Michigan - Ann Arbor** (*Sept/2019 - May/2022*)\
*Major in Computer Science*

- GPA: 4.0
- Courses:
  - Math 217: Linear Algebra
  - Stats 412: Intro to Probability & Statistics
  - Math 412: Intro to Modern Algebra
  - EECS 281: Data Structures and Algorithms
  - EECS 370: Introduction to Computer Organization
  - EECS 376: Foundations of Computer Science
  - EECS 484: Database System

### Projects

---
**Software Development Engineer Intern @ ByteDance**\
*Data-Ads system, June/2020 - August/2020*

- Participated in the development of automatic advertising debugging tools, added modular displaying feature to improve the practicality of the tool, which received extensive usage inside the company.
- Maintained and further developed the advertising business feedback oncall system, developed case aging statistics and reminder feature to improve the case solving rate by 20%.
- Participated in the development of a real-time advertising data detection and alarm system which determine the data abnormality in the last hour based on historical data. The system significantly reduced the processing time of the advertising system abnormality by 60%.

**NLP Algorithms Research Intern**\
*Microsoft STCA, May/2020 - June/2020*

- Survey the newest development and implementation of NLP algorithms in Knowledge Base Question Answering system, share the results with group members.
- Survey the state-of-the-art approaches in multi-lingual NLP training, proposed methods to train and evaluate multi-lingual KBQA system, especially in zero-shot situation.
- Collected and organised the commonly used Knowledge Base and data set in KBQA task for our system, filtered the data set and Knowledge Base to generate answer candidates for quick searching.
- Implemented the Transformer based methods in KBQA tasks and discussed the advantages and disadvantages of such methods.

**Research Project: Pruning Multi-view Stereo Network for Efficient 3D Reconstruction**\
*Undergraduate Research with Xiang Xiang@JHU*

- Devised new approach to compress and accelerate Convolutional Neural Networks(CNNs) in 3D reconstruction.
- Proposed a large multi-scale architecture for exploiting efficiency in 3D CNNs, and tested the proposed network
with Tensorflow in Python.
- Achieved an efficient Multiview 3D reconstruction system up to 2 times faster, in contrast to the state-of-the-art,
while maintaining comparable model accuracy and even better completeness and generalize ability.
- Created web blogs about related papers and studies. Wrote original contents about researches and basic theories
in Machine Learning, which improved understanding of team members.

### Publication

---

- **Pruning Multi-view Stereo Net for Efficient 3D Reconstruction**\
  Xiang Xiang, ***Zhiyuan Wang***, Shanshan Lao, Baochang Zhang\
  *In the ISPRS Journal of Photogrammetry and Remote Sensing (ISPRS 2020)*
  
### Skill Keywords

---
{% for skill in site.data.skills %}
- {{ skill.name }}
<div class="btn-inline">
{% for keyword in skill.keywords %}
<button class="btn btn-outline" type="button">{{ keyword }}</button>
{% endfor %}
</div>
{% endfor %}


### Contact

<ul>
{% for website in site.data.social %}
<li>{{website.sitename }}：<a href="{{ website.url }}" target="_blank">@{{ website.name }}</a></li>
{% endfor %}
</ul>

