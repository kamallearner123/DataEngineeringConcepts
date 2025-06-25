from .views import book_view, tutorials_dashboard
from django.urls import path
from .views import python_book
from .views import display_page

# URL patterns
urlpatterns = [
    path('', tutorials_dashboard, name='tutorials_dashboard'),
    #path('tutorials/topic <str:topic>/<path:subtopic>/', book_view, name='book_detail'),
    path('<str:topic>/', book_view, name='tutorials'),
    # include path to just display page from directory Topics/course/<str:topic>/
    path('courses/<str:topic>/', book_view, name='course_topic'),  # Handles /course/topic/
    path('<str:topic>/<str:subtopic>/', book_view, name='book_detail'),
    # path('python/', python_book, name='python_course'),  # Handles /python/
    path('file_path/<path:file_path>/', display_page, name='tutorials'),

]


'''
Topic: 
Create html page about the above topics with interesting points and challenge questions.
'''