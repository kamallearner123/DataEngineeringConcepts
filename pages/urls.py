from .views import book_view
from django.urls import path

# URL patterns
urlpatterns = [
    path('', book_view, name='book_home'),
    path('topic <str:topic>/<str:subtopic>/', book_view, name='book_detail'),
]

# Create html page about the above topics with interesting points and challenge questions.
