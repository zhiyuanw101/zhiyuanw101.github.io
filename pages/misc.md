---
layout: page
title: Misc
description: 人越学越觉得自己无知
keywords: 维基, Misc
comments: false
menu: 维基
permalink: /misc/
---

> 「有研究顯示，打字的時候不喜歡在中文和英文之間加空格的人，感情路都走得很辛苦，有七成的比例會在 34 歲的時候跟自己不愛的人結婚，而其餘三成的人最後只能把遺產留給自己的貓。畢竟愛情跟書寫都需要適時地留白。」——vinta/paranoid-auto-spacing

<ul class="listing">
{% for misc in site.misc %}
{% if misc.title != "Wiki Template" and misc.topmost == true %}
<li class="listing-item"><a href="{{ site.url }}{{ misc.url }}"><span class="top-most-flag">[置顶]</span>{{ misc.title }}</a></li>
{% endif %}
{% endfor %}
{% for misc in site.misc %}
{% if misc.title != "Wiki Template" and misc.topmost != true %}
<li class="listing-item"><a href="{{ site.url }}{{ misc.url }}">{{ misc.title }}<span style="font-size:12px;color:red;font-style:italic;">{%if misc.layout == 'mindmap' %}  mindmap{% endif %}</span></a></li>
{% endif %}
{% endfor %}
</ul>
