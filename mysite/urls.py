from django.contrib import admin
from django.urls import path, include
from blog.Microphone import home
urlpatterns = [
    path("", home),
    path("admin/", admin.site.urls),
    path("", include("blog.urls")),
]