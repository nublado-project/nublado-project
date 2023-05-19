from django.urls import path

from .views import (
    HomeView,
    HealthView
)

app_name = 'project_app'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('health', HealthView.as_view(), name='health')
]
