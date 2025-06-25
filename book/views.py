from django.shortcuts import render

# Create your views here.
def book_view(request, topic=None, subtopic=None):
    """
    View to render the book page with the selected topic and subtopic.
    If no topic or subtopic is provided, it defaults to the first available topic and subtopic.
    """
    # Define the directory where HTML pages are stored
    HTML_TOPICS_PAGES_DIR = 'Topics/course'
    
    # Get the directory structure for the topics
    structure = {}
    if topic:
        structure[topic] = [f for f in os.listdir(os.path.join(HTML_TOPICS_PAGES_DIR, topic)) if f.endswith('.html')]
    
    # If no topic is selected, use the first topic and its first subtopic
    if not subtopic and structure:
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