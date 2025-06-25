from .views import book_view
from django.urls import path

# URL patterns for the book app
# This will handle URLs like /book/<str:topic>/
# where <str:topic> is a placeholder for the topic name.
# The book_view function will be called to handle these requests.
urlpatterns = [
    # Include the URLs from the book app
    path('<str:topic>/', book_view, name='book_detail'),
]
