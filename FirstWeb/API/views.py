from django.shortcuts import render
from django.http import HttpResponse
import yfinance as yf
import json
from django.contrib.auth.decorators import login_required


# Create your views here.

@login_required
def index(response,id):
    stock = yf.Ticker(str(id).upper())
    dictstock = list(zip(stock.info.keys(),stock.info.values()))
    html = "<ul>"
    for item in dictstock:
        html += "<li>"+ str(item) +"</li>"
    html +="</ul>"

    return HttpResponse(html)
def home(response):
    return HttpResponse("<h1>API HOME<h1>")