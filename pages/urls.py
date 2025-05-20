from .views import book_view
from django.urls import path

# URL patterns
urlpatterns = [
    path('', book_view, name='book_home'),
    path('topic <str:topic>/', book_view, name='book_topic'),
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