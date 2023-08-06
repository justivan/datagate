from django.shortcuts import render
from django.conf.urls import handler404, handler500


def index(request):
    return render(request, "pages/index.html")
