"""
URL configuration for DataEngineering project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from .views import login_view, register_view
from django.contrib.auth.decorators import login_required
import book

def home_page(request):
    return render(request, "home/home.html")  # ✅ matches your template path

def course_rpi_python(request):
    return render(request, "courses/python_for_beginners.html")  # ✅ matches your template path


urlpatterns = [
    path("admin/", admin.site.urls),
    # when user open the browser and type localhost:8000, it will redirect to home page with is there in tempaltes/home/home.html
    path("", home_page, name="home"),
    path("tutorials/", include("pages.urls")),  # Include the URLs from the book app
    path("tutorials/<str:topic>/", include("pages.urls")),  # Include the URLs from the book app with topic
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('course_rpi_python/', course_rpi_python, name='course_rpi_python'),
    path('book_view', include('book.urls')),  # Include the URLs from the book app
]