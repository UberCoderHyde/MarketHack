from celery import shared_task
from celery.decorators import task
from .models import Stock
from bs4 import BeautifulSoup
from urllib.request import urlopen  
import requests
import re
from datetime import datetime
import django
django.setup()
# Json SEARCH WORK ==== earningsDate
# ENDPOINT LINK ===="https://query2.finance.yahoo.com/v10/finance/quoteSummary/" + stockSymbol + "?modules=assetProfile,balanceSheetHistory,balanceSheetHistoryQuarterly,calendarEvents,cashflowStatementHistory,cashflowStatementHistoryQuarterly,defaultKeyStatistics,earnings,earningsHistory,earningsTrend,financialData,fundOwnership,incomeStatementHistory,incomeStatementHistoryQuarterly,indexTrend,industryTrend,insiderHolders,insiderTransactions,institutionOwnership,majorDirectHolders,majorHoldersBreakdown,netSharePurchaseActivity,price,quoteType,recommendationTrend,secFilings,sectorTrend,summaryDetail,summaryProfile,symbol,upgradeDowngradeHistory,fundProfile,topHoldings,fundPerformance" 

@shared_task(name = "quarterlyUpdateChecker")
def checker(stockSymbol):
    stockdata = Stock.objects.get(symbol = stockSymbol)
    stockMostRecentQuarter = stockdata.recentQuarter
    url = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/" + stockSymbol + "?modules=assetProfile,balanceSheetHistory,balanceSheetHistoryQuarterly,calendarEvents,cashflowStatementHistory,cashflowStatementHistoryQuarterly,defaultKeyStatistics,earnings,earningsHistory,earningsTrend,financialData,fundOwnership,incomeStatementHistory,incomeStatementHistoryQuarterly,indexTrend,industryTrend,insiderHolders,insiderTransactions,institutionOwnership,majorDirectHolders,majorHoldersBreakdown,netSharePurchaseActivity,price,quoteType,recommendationTrend,secFilings,sectorTrend,summaryDetail,summaryProfile,symbol,upgradeDowngradeHistory,fundProfile,topHoldings,fundPerformance"
    page = urlopen(url)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    stringBS=soup.get_text()
    searchTERM1 ="mostRecentQuarter\":\{\"raw\":(.*?),\"fmt\":"
    mostRecentQuarter = datetime.fromtimestamp(int(re.search(searchTERM1, stringBS).group(1)))
    if not stockMostRecentQuarter:
        stockdata.recentQuarter = stockMostRecentQuarter
        stockdata.save()
    searchTERM = "earningsDate\":\[\{\"raw\":(.*?),\"fmt\":"
    testingSearchTerm = "earningsDate"
    if testingSearchTerm in stringBS:
        earningsDateText = datetime.fromtimestamp(int(re.search(searchTERM, stringBS).group(1)))
        if (int(re.search(searchTERM, stringBS).group(1)) <=  int(re.search(searchTERM1, stringBS).group(1))):
            stockdata.recentQuarter = stockMostRecentQuarter
            stockdata.save()
