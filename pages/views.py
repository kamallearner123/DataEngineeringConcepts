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
HTML_PYTHON_PAGES_DIR = os.path.join(settings.BASE_DIR, 'Topics', 'data_engineering')
HTML_TOPICS_PAGES_DIR = os.path.join(settings.BASE_DIR, 'Topics') # Ensure it's an absolute path
HTML_PAGES_AGENTICAI_DIR = os.path.join(settings.BASE_DIR, 'Topics', 'agenticai')
HTML_PAGES_SYSTEM_PROGRAMMING_DIR = os.path.join(settings.BASE_DIR, 'Topics', 'system_programming')
# add pathf for rust_programming
HTML_PAGES_RUST_PROGRAMMING_DIR = os.path.join(settings.BASE_DIR, 'Topics', 'rust_programming')
HTML_PAGES_THOUGHT_FOR_THE_DAY_DIR = os.path.join(settings.BASE_DIR, 'Topics', 'thought_for_the_day')
HTML_PAGE_COURSE_DIR = os.path.join(settings.BASE_DIR, 'Topics', 'courses')


from collections import defaultdict

def build_structure(file_list):
    structure = defaultdict(lambda: defaultdict(list))

    for filepath in file_list:
        parts = filepath.split('/')
        if len(parts) == 2:
            topic, file = parts
            structure[topic]['_files'].append(file)
        elif len(parts) == 3:
            topic, subfolder, file = parts
            structure[topic][subfolder].append(file)

    return dict(structure)

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

    # Walk through all subdirectories and collect HTML files
    for root, dirs, files in os.walk(pages_dir):
        # Get the relative path from pages_dir to current root
        rel_path = os.path.relpath(root, pages_dir)
        if rel_path == ".":
            topic = os.path.basename(pages_dir)
        else:
            topic = rel_path.split(os.sep)[0]
        if topic not in structure:
            structure[topic] = []
        # Only add HTML files that are directly under this root
        html_files = [f for f in files if f.endswith('.html')]
        html_files.sort(key=numeric_key)
        # Store files with their relative path from the topic folder
        for f in html_files:
            # Get the path relative to the topic folder
            file_rel_path = os.path.relpath(os.path.join(root, f), os.path.join(pages_dir, topic))
            structure[topic].append(file_rel_path)
    # Sort topics
    structure = dict(sorted(structure.items(), key=lambda x: numeric_key(x[0])))
    # Sort subtopics for each topic
    for topic in structure:
        structure[topic].sort(key=numeric_key)

    logging.info(f"Directory structure: {structure}")

    final_list = []
    for topic, subtopics in structure.items():
        # Create a list of tuples (topic, subtopic)
        for subtopic in subtopics:
            final_list.append(os.path.join(topic, subtopic))

    final_list = build_structure(final_list)
    
    return final_list

def python_book(request):
    """Render the Python book page with sidebar and content."""
    structure = get_directory_structure(HTML_PYTHON_PAGES_DIR)
    
    # If no topic is selected, use the first topic and its first subtopic
    topic = list(structure.keys())[0] if structure else None
    subtopic = structure[topic][0] if topic and structure[topic] else None
    
    # Read the content of the selected HTML file
    content = ""
    if topic and subtopic:
        file_path = os.path.join(HTML_PYTHON_PAGES_DIR, topic, subtopic)
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

def display_page(request, topic):
    """Display a specific HTML page based on the topic."""
    file_path = os.path.join(HTML_TOPICS_PAGES_DIR, topic)
    print(f"File path: {file_path}")
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return HttpResponse(content)
    else:
        return HttpResponse("<p>File not found.</p>", status=404)

def book_view(request, topic=None, subtopic=None):
    print(f"****** Requested topic: {topic} and subtopic: {subtopic}")
    """Render the book page with sidebar and content."""
    if topic == "agenticai":
        structure = get_directory_structure(HTML_PAGES_AGENTICAI_DIR)
    elif topic == "data_engineering":
        structure = get_directory_structure(HTML_PYTHON_PAGES_DIR)
    elif topic == "system_programming":
        structure = get_directory_structure(HTML_PAGES_SYSTEM_PROGRAMMING_DIR)
    elif topic == "thought_for_the_day":
        # For "thought_for_the_day", we can return a static page or handle it differently
        structure = get_directory_structure(HTML_PAGES_THOUGHT_FOR_THE_DAY_DIR)
    elif topic == "rust_programming":
        structure = get_directory_structure(HTML_PAGES_RUST_PROGRAMMING_DIR)
    elif topic.startswith("course"):
        # For "course", we can return a static page or handle it differently
        structure = get_directory_structure(HTML_PAGE_COURSE_DIR)
    else:
        structure = get_directory_structure(HTML_PAGES_DIR)
    
    # # If no topic is selected, use the first topic and its first subtopic
    # if not subtopic and structure:
    #     topic = structure.keys())[0]
    #     subtopic = structure[topic][0] if structure[topic] else None

    
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

    # Example structure transformation in your Django view
    clean_structure = {}

    for topic, items in structure.items():
        clean_items = {}
        for key, value in items.items():
            if key == "_files":
                clean_items["root_files"] = value  # Rename _files -> root_files
            else:
                clean_items[key] = value
        clean_structure[topic] = clean_items

    context = {
        'structure': clean_structure,
        'selected_topic': topic,
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