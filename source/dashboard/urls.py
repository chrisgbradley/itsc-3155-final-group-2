from django.urls import path
from . import views
from .dash_apps import tuition

urlpatterns = [
    path('', views.home, name='dashboard'),
    path('about', views.about),
    path('dashboard/', views.dashboard),
    path('dashboard/boards/tuition/', views.tuition),
    path('dashboard/boards/admissions/', views.admissions),
    path('dashboard/boards/degrees/', views.degrees),
    path('dashboard/boards/loansgrants/', views.loansgrants),
]
