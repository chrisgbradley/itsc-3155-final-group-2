from django.shortcuts import render

# Create your views here.

def home(requests):
    return render(requests, 'dashboard/welcome.html')