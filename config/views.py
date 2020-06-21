from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def inde(request):
    x ="<h1>wangyuxuan</h1>"
    return HttpResponse(x)