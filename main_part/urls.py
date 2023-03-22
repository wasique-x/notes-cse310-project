"""main_part URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib.auth.views import LogoutView

from note_part.views import (
    home,
    edit_note,
    trash_note,
    archive_note,
    view_trash,
    view_archive,
    untrash_note,
    unarchive_note,
    delete_note,
    CustomLoginView,
    CustomRegisterView,
    about,
)

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="login"), name="logout"),
    path("register/", CustomRegisterView.as_view(), name="register"),
    path("about/", about, name="about"),
    
    path("", home, name="home"),
    path("notes/", edit_note, name="edit_note"),
    path("trash_note/<int:note_id>/", trash_note, name="trash_note"),
    path("archive_note/<int:note_id>/", archive_note, name="archive_note"),
    path("trash/", view_trash, name="view_trash"),
    path("untrash_note/<int:note_id>/", untrash_note, name="untrash_note"),
    path("delete_note/<int:note_id>/", delete_note, name="delete_note"),
    path("archive/", view_archive, name="view_archive"),
    path("unarchive_note/<int:note_id>/", unarchive_note, name="unarchive_note"),
    path("admin/", admin.site.urls),
]
