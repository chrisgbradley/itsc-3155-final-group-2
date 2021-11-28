from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from flask import render_template

# Create your views here.


def home(requests):
    return render(requests, 'dashboard/home.html')


def dashboard(requests):
    response = HttpResponse(status=302)
    response['Location'] = 'boards/tuition'
    return response


def tuition(requests):
    return render(requests, 'dashboard/boards/tuition.html', {'tuition': 'selected'})


def admissions(requests):
    return render(requests, 'dashboard/boards/admissions.html', {'admissions': 'selected'})


def degrees(requests):
    return render(requests, 'dashboard/boards/degrees.html', {'degrees': 'selected'})


def loansgrants(requests):
    return render(requests, 'dashboard/boards/loansgrants.html', {'loansgrants': 'selected'})