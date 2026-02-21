{% load i18n %}
{% extends "base.html" %}

{% block title %}{% translate "Home" %} — {{PROJECT_NAME}}{% endblock %}

{% block content %}
    <h1>{{PROJECT_NAME}}</h1>
    <p>{% translate "Project is running. Edit templates/home/home.html to get started." %}</p>
{% endblock %}
