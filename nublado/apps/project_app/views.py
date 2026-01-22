from django.views.generic import View, TemplateView
from django.http import JsonResponse


class HomeView(TemplateView):
    template_name = "home.html"


class HealthView(View):

    def get(self, request, *args, **kwargs):
        return JsonResponse({"message": "OK"}, status=200)
