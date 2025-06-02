import os
from django.urls import path
from django.shortcuts import render, redirect
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import logging
import re


# Define the path to the HTML pages directory
HTML_PAGES_DIR = os.path.join(settings.BASE_DIR, 'Topics', 'data_engineering')
HTML_TOPICS_PAGES_DIR = os.path.join(settings.BASE_DIR, 'Topics') # Ensure it's an absolute path
HTML_PAGES_AGENTICAI_DIR = os.path.join(settings.BASE_DIR, 'Topics', 'agenticai')
HTML_PAGES_SYSTEM_PROGRAMMING_DIR = os.path.join(settings.BASE_DIR, 'Topics', 'system_programming')
# add pathf for rust_programming
HTML_PAGES_RUST_PROGRAMMING_DIR = os.path.join(settings.BASE_DIR, 'Topics', 'rust_programming')
HTML_PAGES_THOUGHT_FOR_THE_DAY_DIR = os.path.join(settings.BASE_DIR, 'Topics', 'thought_for_the_day')

def get_directory_structure(pages_dir):
    """Scan the html_pages directory and return a dictionary of topics and subtopics in numeric order."""
    structure = {}
    # Check if pages_dir exists
    logging.info(f"Checking directory: {pages_dir}")
    if not os.path.exists(pages_dir):
        logging.error(f"Directory {pages_dir} does not exist.")
        return structure

    def numeric_key(name):
        """Extract numeric prefix for sorting (e.g., '1.10 Sets.html' -> (1, 10), '1.2 Variables.html' -> (1, 2))."""
        match = re.match(r'^(\d+)\.(\d*)\.?', name)
        if match:
            major = int(match.group(1))  # First part (e.g., '1' in '1.10')
            minor = int(match.group(2) or 0)  # Second part (e.g., '10' in '1.10', or 0 if no minor part)
            return (major, minor)
        return (float('inf'), 0)  # Non-numeric names go to the end

    # Get sorted list of folders
    folders = [f for f in os.listdir(pages_dir) if os.path.isdir(os.path.join(pages_dir, f))]
    folders.sort(key=numeric_key)

    for folder in folders:
        folder_path = os.path.join(pages_dir, folder)
        structure[folder] = []
        # Get sorted list of HTML files
        files = [f for f in os.listdir(folder_path) if f.endswith('.html')]
        files.sort(key=numeric_key)
        structure[folder] = files

    logging.info(f"Directory structure: {structure}")
    return structure

def book_view(request, topic=None, subtopic=None):
    print(f"Requested topic: {topic} and subtopic: {subtopic}")
    """Render the book page with sidebar and content."""
    if topic == "agenticai":
        structure = get_directory_structure(HTML_PAGES_AGENTICAI_DIR)
    elif topic == "system_programming":
        structure = get_directory_structure(HTML_PAGES_SYSTEM_PROGRAMMING_DIR)
    elif topic == "thought_for_the_day":
        # For "thought_for_the_day", we can return a static page or handle it differently
        structure = get_directory_structure(HTML_PAGES_THOUGHT_FOR_THE_DAY_DIR)
    elif topic == "rust_programming":
        structure = get_directory_structure(HTML_PAGES_RUST_PROGRAMMING_DIR)
    else:
        structure = get_directory_structure(HTML_PAGES_DIR)
    
    # If no topic is selected, use the first topic and its first subtopic
    if not topic and structure:
        topic = list(structure.keys())[0]
        subtopic = structure[topic][0] if structure[topic] else None
    
    # Read the content of the selected HTML file
    content = ""
    if topic and subtopic:
        file_path = os.path.join(HTML_TOPICS_PAGES_DIR, topic, subtopic)
        print(f"File path: {file_path}")
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


# Return Tutorials page /template/dashboards/tutorials_dashboard.html
def tutorials_dashboard(request):
    return render(request, 'dashboards/tutorials_dashboard.html')

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