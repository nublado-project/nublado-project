from django.urls import path
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView

from .views import (
    HomeView,
    HealthView
)

app_name = 'project_app'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('health', HealthView.as_view(), name='health'),
	#path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('favicon.ico')))
]
