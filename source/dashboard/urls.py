from django.urls import path
from . import views
from .dash_apps import tuition
from .dash_apps import acceptance_rate
from .dash_apps import gender
from .dash_apps import completion_rate

urlpatterns = [
    path('', views.home, name='dashboard'),
    path('about', views.about),
    path('dashboard/', views.dashboard),
    path('dashboard/boards/tuition/', views.tuition),
    path('dashboard/boards/acceptance_rate/', views.acceptance_rate),
    path('dashboard/boards/gender/', views.gender),
    path('dashboard/boards/completion_rate/', views.completion_rate),
]
