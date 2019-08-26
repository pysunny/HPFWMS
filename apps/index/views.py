from django.shortcuts import render
from django.views.generic import View
from utils.mixin import LoginRequiredMixin

# Create your views here.

class IndexView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'index/index.html')

class WelcomeView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'index/welcome.html')