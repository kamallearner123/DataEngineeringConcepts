from .views import book_view, tutorials_dashboard
from django.urls import path

# URL patterns
urlpatterns = [
    path('', tutorials_dashboard, name='tutorials_dashboard'),
    path('tutorials/<str:topic>/', book_view, name='tutorials'),  # Handles /tutorials/topic%20agenticai/
    path('tutorials/<str:topic>/<str:subtopic>/', book_view, name='tutorials_with_subtopic'),  # Optional subtopic
    # include path to just display page from directory Topics/course/<str:topic>/
    path('courses/<str:topic>/', book_view, name='course_topic'),  # Handles /course/topic/
    
    
    # How to add a subtopic to the URL pattern? example with UTL 127.0.0.1:8080/topic <str:topic>/<str:subtopic>/

    # path('topic <str:topic>/<str:subtopic>/', book_view, name='book_detail'),
    # Example URL:
    # http://127.0.0.1:8000/topic <str:topic>/<str:subtopic>/

    path('topic <str:topic>/<str:subtopic>/', book_view, name='book_detail'),
]


'''
Topic: 
Create html page about the above topics with interesting points and challenge questions.
'''