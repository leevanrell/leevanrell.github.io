---
layout: about
---
{%- if page.title -%}
  <h1 class="page-heading">{{ page.title }}</h1>
{%- endif -%}

<h2 class="post-title">About Me</h2>
<div class="container-block">
<div class="main">
    {% include cv/career-profile.html %}
    {% include cv/experience.html %}
    <!-- {% include cv/projects.html %} -->
    {% include cv/education.html %}
    <!-- {% include cv/publications.html %} -->
    {% include cv/skills.html %}
    {% include cv/languages.html %}
</div>
</div>