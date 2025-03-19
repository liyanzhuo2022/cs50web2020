"""
URL configuration for lecture3 project.

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
from django.urls import include, path

# The urls.py file in the lecture3 project is the main URL configuration file for the entire project.
# It includes the URL patterns for the admin interface and the hello app.
# The urls.py file in the hello app is specific to the hello app and defines the URL patterns for the views in that app.
urlpatterns = [
    path("admin/", admin.site.urls),
    path("hello/", include("hello.urls")),
    path("newyear/", include("newyear.urls")),
    path("tasks/", include("tasks.urls")),
] 

