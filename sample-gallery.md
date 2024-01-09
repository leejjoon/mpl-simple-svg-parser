---
layout: single
title: Sample Gallery
permalink: /gallery/
---

{% assign gallery = site.data.gallery %}

{% assign gallery_layout = '' %}

<figure class="{{ gallery_layout }} {{ include.class }}">
  {% for img in gallery %}
    {% if img.url %}
      <a href="{{ img.url | relative_url }}"
        {% if img.title %}title="{{ img.title }}"{% endif %}>
          <img src="{{ img.image_path | relative_url }}"
               alt="{% if img.alt %}{{ img.alt }}{% endif %}">
      </a>
    {% else %}
      <img src="{{ img.image_path | relative_url }}"
           alt="{% if img.alt %}{{ img.alt }}{% endif %}">
    {% endif %}
  {% endfor %}
</figure>
