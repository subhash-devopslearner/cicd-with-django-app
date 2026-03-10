from django.shortcuts import render
from django.http import HttpResponse
import os

# Create your views here.
def home(request):
    environment = os.getenv('ENVIRONMENT', 'development')
    return HttpResponse(f'Welcome to CICD testing with Django app 🚀 (Environment: {environment})')