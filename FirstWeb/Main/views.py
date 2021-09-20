from django.shortcuts import render, redirect
from django.http import HttpResponse
import yfinance as yf
import json
from yahoo_fin import stock_info as si
from datetime import datetime
from threading import Thread
from contextlib import suppress
import math
from Main.models import Stock
import csv
import io
from django.core.files import File
from django.contrib.auth.decorators import login_required
import time
from bs4 import BeautifulSoup
from urllib.request import urlopen  
import requests
import re
from .tasks import checker
from django.http import JsonResponse
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.core.cache import cache
# Create your views here.

def stock(request,name):
    if name == "undefined":
        return redirect("http://127.0.0.1:8000")
    #name = request.get_host()+request.path
    addList = ["Home","News","Trending","Sectors","Account","Discord"]
    urlList = ["http://127.0.0.1:8000/","http://127.0.0.1:8000/new/","http://127.0.0.1:8000/trending/","http://127.0.0.1:8000/sectors/","http://127.0.0.1:8000/account/","https://discord.com/invite/NY97VQbURH"]
    if name in addList:
        return redirect(urlList[addList.index(name)])
    if not Stock.objects.filter(symbol = name).exists():
        tempStockObject = Stock.objects.get(fullName = name)
        stockSymbol = tempStockObject.symbol
        stockSymbol = stockSymbol.replace(" ","")
        return redirect("http://127.0.0.1:8000/stock/"+stockSymbol)
#    checker.delay(name)
    dictstock={'stock':name}
    dictstock['name'] = name
    
    
# trailingPE = PE Ratio
# priceToBook = Price To Book = https://query2.finance.yahoo.com/v10/finance/quoteSummary/+ StockTicker +?modules=incomeStatementHistoryQuarterly
# debtToEquity = DE =https://query2.finance.yahoo.com/v10/finance/quoteSummary/+ StockTicker +?modules=assetProfile,balanceSheetHistory,balanceSheetHistoryQuarterly,calendarEvents,cashflowStatementHistory,cashflowStatementHistoryQuarterly,defaultKeyStatistics,earnings,earningsHistory,earningsTrend,financialData,fundOwnership,incomeStatementHistory,incomeStatementHistoryQuarterly,indexTrend,industryTrend,insiderHolders,insiderTransactions,institutionOwnership,majorDirectHolders,majorHoldersBreakdown,netSharePurchaseActivity,price,quoteType,recommendationTrend,secFilings,sectorTrend,summaryDetail,summaryProfile,symbol,upgradeDowngradeHistory,fundProfile,topHoldings,fundPerformance
# freeCashFlow = FCF = https://query2.finance.yahoo.com/v10/finance/quoteSummary/+ StockTicker +?modules=assetProfile,balanceSheetHistory,balanceSheetHistoryQuarterly,calendarEvents,cashflowStatementHistory,cashflowStatementHistoryQuarterly,defaultKeyStatistics,earnings,earningsHistory,earningsTrend,financialData,fundOwnership,incomeStatementHistory,incomeStatementHistoryQuarterly,indexTrend,industryTrend,insiderHolders,insiderTransactions,institutionOwnership,majorDirectHolders,majorHoldersBreakdown,netSharePurchaseActivity,price,quoteType,recommendationTrend,secFilings,sectorTrend,summaryDetail,summaryProfile,symbol,upgradeDowngradeHistory,fundProfile,topHoldings,fundPerformance
# priceEarningsToGrowth = PEG = 
    trailingPE= 1
    priceToBook = 2
    debtToEquity = 3
    freeCashFlow = 4
    priceEarningsToGrowth = 5
    dictstock['PERatio']=trailingPE
    dictstock['priceToBook'] = priceToBook
    dictstock['DE'] = debtToEquity
    dictstock['FCF'] = freeCashFlow
    dictstock['PEG'] = priceEarningsToGrowth
    return render(request,'baseStock.html',dictstock)
def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)
    return next_month - datetime.timedelta(days=next_month.day)
def home(response):
    return render(response, "home.html")
def test(response):
    return render(response,'test.html',context = {'text' : "HELLO WORLD"})
def news(response):
    return render(response,'news.html')
def trending(response):
    return render(response,'trending.html')
def sectors(response):
    return render(response,'sectors.html')
def search_address(request):
    symbol = request.GET.get('symbol')
    symbol = symbol.replace(" ","")
    payload = []
    addList = []
    if symbol:
        counter = 0
        stockObject = Stock.objects.filter(symbol__icontains=symbol)
        for stockObject in stockObject:
            if counter >=10:
                break
            else:
                payload.append(stockObject.symbol)
                counter +=1

    if symbol:
        zcounter = 0
        stockObject = Stock.objects.filter(fullName__icontains=symbol)
        for stockObject in stockObject:
            if zcounter >=10:
                break
            else:
                payload.append(stockObject.fullName)
                zcounter += 1
                addList = ["Home","News","Trending","Sectors","Account","Discord"]
        for word in addList:
            payload.append(word)
    return JsonResponse({'status' : 200 , 'data' : payload})    