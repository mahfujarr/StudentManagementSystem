"""
URL configuration for ZCA project.

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
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('list', list, name='student-list'),
    path('add', add, name='student-add'),
    path('edit', edit, name='student-edit'),
    path('details/<str:student_id>', details, name='student-details'),
    path('fees_collections', fees_collections, name='fees-collections'),
    path('add_fees_collection', add_fees_collection, name='add-fees-collection'),
    path('register-new-admin', register_new_admin, name='register-new-admin'),
]
