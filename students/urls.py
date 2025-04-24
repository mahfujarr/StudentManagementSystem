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
    path('edit/<str:student_id>', edit, name='student-edit'),
    path('details/<str:student_id>', details, name='student-details'),
    path('delete/<str:student_id>', delete_student, name='student-delete'),
    path('add_payment/<str:student_id>', delete_student, name='add-payment'),
    path('fees_collections', fees_collections, name='fees-collections'),
    path('add_fees_collection', add_fees_collection, name='add-fees-collection'),
    path('view-fees', view_fees, name='view-fees'),
    path('login', login, name='login'),
    path('forgot-password', forgot_password, name='forgot-password'),
    path('register-new-admin', register_new_admin, name='register-new-admin'),
]
