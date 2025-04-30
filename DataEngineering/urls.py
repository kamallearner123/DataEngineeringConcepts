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


def home_page(request):
    return render(request, "home/home.html")  # ✅ matches your template path


urlpatterns = [
    path("admin/", admin.site.urls),
    # when user open the browser and type localhost:8000, it will redirect to home page with is there in tempaltes/home/home.html
    path("", home_page, name="home"),
]