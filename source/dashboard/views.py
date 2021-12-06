from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from flask import render_template

# Create your views here.


def home(requests):
    return render(requests, 'dashboard/home.html')

def about(requests):
    return render(requests, 'dashboard/about.html')


def dashboard(requests):
    response = HttpResponse(status=302)
    response['Location'] = 'boards/tuition'
    return response


def tuition(requests):
    return render(requests, 'dashboard/boards/tuition.html', {'tuition': 'selected'})


def acceptance_rate(requests):
    return render(requests, 'dashboard/boards/acceptance_rate.html', {'acceptance_rate': 'selected'})


def gender(requests):
    return render(requests, 'dashboard/boards/gender.html', {'gender': 'selected'})


def completion_rate(requests):
    return render(requests, 'dashboard/boards/completion_rate.html', {'completion_rate': 'selected'})