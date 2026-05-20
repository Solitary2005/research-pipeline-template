---
layout: default
title: "Favorites"
permalink: /favorites/
---

# 📌 Favorite Papers

Papers you've archived. Browse by topic or revisit anytime.

{% assign interesting_papers = site.papers | where_exp: "paper", "paper.interesting == true" | sort: "published_date" | reverse %}

{% if interesting_papers.size == 0 %}
<div class="empty-state">
  <p>No papers have been archived yet.</p>
  <p><a href="{{ site.baseurl }}/">Browse today's papers</a> and request a summary to add them here.</p>
</div>
{% else %}

{% assign topics = interesting_papers | map: "topic" | uniq | sort %}

{% if topics.size > 1 %}
<div class="topic-nav">
  <span>Jump to: </span>
  {% for topic in topics %}
  <a href="#topic-{{ topic | slugify }}">{{ topic }}</a>{% unless forloop.last %} · {% endunless %}
  {% endfor %}
</div>
{% endif %}

{% for topic in topics %}
## 📂 {{ topic }}{: #topic-{{ topic | slugify }} }

{% assign topic_papers = interesting_papers | where_exp: "paper", "paper.topic == topic" %}

{% for paper in topic_papers %}
<div class="paper-card">
  <div class="paper-card-date">{{ paper.published_date }}</div>
  <h2><a href="{{ site.baseurl }}{{ paper.url }}">{{ paper.title }}</a></h2>
  <div class="paper-card-authors">{{ paper.authors }}</div>
  <a class="btn-read" href="{{ site.baseurl }}{{ paper.url }}">Read more →</a>
  {% if paper.has_podcast %}
  <a class="btn-listen" href="{{ site.baseurl }}/podcasts/{{ paper.arxiv_id }}/">🎧 Listen to Podcast</a>
  {% endif %}
</div>
{% endfor %}

{% endfor %}

<p class="favorites-count">{{ interesting_papers.size }} paper{% if interesting_papers.size != 1 %}s{% endif %} archived across {{ topics.size }} topic{% if topics.size != 1 %}s{% endif %}.</p>

{% endif %}
