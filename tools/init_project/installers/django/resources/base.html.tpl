{% load i18n %}
<!DOCTYPE html>
<html lang="{{ LANGUAGE_CODE }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}{{ site_settings.meta_title }}{% endblock %}</title>
    <meta name="description" content="{% block meta_description %}{{ site_settings.meta_description }}{% endblock %}">
    <link rel="icon" type="image/x-icon" href="{{ site_settings.favicon_url }}">

    {% load static %}
    <link rel="stylesheet" href="{% static 'css/app.css' %}">
    {% block extra_css %}{% endblock %}
</head>
<body>
    <main>
        {% block content %}{% endblock %}
    </main>

    {% block extra_js %}{% endblock %}
</body>
</html>
