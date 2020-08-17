---
layout: page
title: About
description: 
keywords: Zhiyuan Wang
comments: true
menu: 关于
permalink: /about/
---

>>Hi! This is Zhiyuan Wang, an undergraduate studying Computer Science at the University of Michigan, Ann Arbor. Love traveling and skiing. Huge fan of Christopher Nolan, Radiohead & Blur. Want to have a dog.

## Contact

<ul>
{% for website in site.data.social %}
<li>{{website.sitename }}：<a href="{{ website.url }}" target="_blank">@{{ website.name }}</a></li>
{% endfor %}
</ul>


## Skill Keywords

{% for skill in site.data.skills %}
### {{ skill.name }}
<div class="btn-inline">
{% for keyword in skill.keywords %}
<button class="btn btn-outline" type="button">{{ keyword }}</button>
{% endfor %}
</div>
{% endfor %}
