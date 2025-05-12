import os
from django.urls import path
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Define the path to the HTML pages directory
HTML_PAGES_DIR = os.path.join(settings.BASE_DIR, 'html_pages')

def get_directory_structure():
    """Scan the html_pages directory and return a dictionary of topics and subtopics in alphanumeric order."""
    structure = {}
    if os.path.exists(HTML_PAGES_DIR):
        for folder in sorted(os.listdir(HTML_PAGES_DIR), key=str.lower):
            folder_path = os.path.join(HTML_PAGES_DIR, folder)
            if os.path.isdir(folder_path):
                structure[folder] = []
                for file in sorted(os.listdir(folder_path), key=str.lower):
                    if file.endswith('.html'):
                        structure[folder].append(file)
    return structure

def book_view(request, topic=None, subtopic=None):
    """Render the book page with sidebar and content."""
    structure = get_directory_structure()
    
    # If no topic is selected, use the first topic and its first subtopic
    if not topic and structure:
        topic = list(structure.keys())[0]
        subtopic = structure[topic][0] if structure[topic] else None
    
    # Read the content of the selected HTML file
    content = ""
    if topic and subtopic:
        file_path = os.path.join(HTML_PAGES_DIR, topic, subtopic)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            content = "<p>File not found.</p>"

    context = {
        'structure': structure,
        'selected_topic': topic,
        'selected_subtopic': subtopic,
        'content': content,
    }
    return render(request, 'book/book.html', context)

@login_required
def user_dashboard(request):
    return render(request, 'dashboards/user_dashboard.html')

# settings.py configuration (add to your settings.py)
"""
INSTALLED_APPS = [
    ...
    'book',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        ...
    }
]

# Define BASE_DIR if not already defined
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
"""

# book/templates/book/book.html
"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Book Viewer</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; display: flex; height: 100vh; }
        .sidebar { width: 250px; background: #f4f4f4; padding: 20px; overflow-y: auto; }
        .sidebar h2 { margin-top: 0; }
        .sidebar ul { list-style: none; padding: 0; }
        .sidebar ul li { margin: 10px 0; }
        .sidebar ul li a { text-decoration: none; color: #333; }
        .sidebar ul li a:hover { color: #007bff; }
        .sidebar .subtopic { margin-left: 20px; }
        .content { flex-grow: 1; padding: 20px; overflow-y: auto; }
        .selected { font-weight: bold; color: #007bff; }
    </style>
</head>
<body>
    <div class="sidebar">
        <h2>Book Contents</h2>
        <ul>
            {% for topic, subtopics in structure.items %}
                <li>
                    <a href="{% url 'book_detail' topic subtopics.0 %}" {% if topic == selected_topic %}class="selected"{% endif %}>{{ topic }}</a>
                    <ul>
                        {% for subtopic in subtopics %}
                            <li class="subtopic">
                                <a href="{% url 'book_detail' topic subtopic %}" {% if subtopic == selected_subtopic and topic == selected_topic %}class="selected"{% endif %}>{{ subtopic }}</a>
                            </li>
                        {% endfor %}
                    </ul>
                </li>
            {% endfor %}
        </ul>
    </div>
    <div class="content">
        {{ content|safe }}
    </div>
</body>
</html>
"""

# book/templates/login.html
"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
</head>
<body>
    <h2>Login</h2>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Login</button>
    </form>
    <p>Don't have an account? <a href="{% url 'register' %}">Register here</a>.</p>
</body>
</html>
"""

# book/templates/register.html
"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Register</title>
</head>
<body>
    <h2>Register</h2>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Register</button>
    </form>
    <p>Already have an account? <a href="{% url 'login' %}">Login here</a>.</p>
</body>
</html>
"""

urlpatterns = [
    path('', book_view, name='book_home'),
    path('book/<str:topic>/', book_view, name='book_topic'),
    path('book/<str:topic>/<str:subtopic>/', book_view, name='book_detail'),
    path('dashboard/', user_dashboard, name='user_dashboard'),
]