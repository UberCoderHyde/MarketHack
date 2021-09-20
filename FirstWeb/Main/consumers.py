from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asyncio import sleep
from random import randint
from urllib.request import urlopen
import requests
import re
from bs4 import BeautifulSoup
import json
import Main.views


class StockConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        temp = self.scope['path'] 
        stock = re.search("/stock/(.*?)/",temp).group(1)
        link =  "https://query1.finance.yahoo.com/v7/finance/quote?lang=en-US&region=US&corsDomain=finance.yahoo.com&symbols="+stock
        link2 = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/"+ stock +"?modules=incomeStatementHistoryQuarterly"
        link3 = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/"+ stock +"?modules=assetProfile,balanceSheetHistory,balanceSheetHistoryQuarterly,calendarEvents,cashflowStatementHistory,cashflowStatementHistoryQuarterly,defaultKeyStatistics,earnings,earningsHistory,earningsTrend,financialData,fundOwnership,incomeStatementHistory,incomeStatementHistoryQuarterly,indexTrend,industryTrend,insiderHolders,insiderTransactions,institutionOwnership,majorDirectHolders,majorHoldersBreakdown,netSharePurchaseActivity,price,quoteType,recommendationTrend,secFilings,sectorTrend,summaryDetail,summaryProfile,symbol,upgradeDowngradeHistory,fundProfile,topHoldings,fundPerformance"

        page3 = urlopen(str(link3))
        html3 = page3.read().decode("utf-8")
        soup3 = BeautifulSoup(html3, "html.parser")
        stringBS2=soup3.get_text()
        searchTermPE = "\"peRatio\":{\"raw\":(.*?),\"fmt\":"
        searchTermPriceToBook = "\"priceToBook\":{\"raw\":(.*?),\"fmt\":\""
        searchTermDE ="\"debtToEquity\":{\"raw\":(.*?),\"fmt\""
        searchTermFCF ="\"freeCashflow\":{\"raw\":(.*?),\"fmt\":"
        searchTermPEG ="\"pegRatio\":{\"raw\":(.*?),\"fmt\":"
        data = {}
        PE = re.search(searchTermPE, stringBS2).group(1)
        PriceToBook = re.search(searchTermPriceToBook, stringBS2).group(1)
        DE = re.search(searchTermDE, stringBS2).group(1)
        FCF = re.search(searchTermFCF, stringBS2).group(1)
        PEG = re.search(searchTermPEG, stringBS2).group(1)
        data["PE"]= PE
        data["PriceToBook"]= PriceToBook
        data["DE"]= DE
        data["FCF"]= FCF
        data["PEG"]= PEG

        while True:
            page = urlopen(str(link))
            html = page.read().decode("utf-8")
            soup = BeautifulSoup(html, "html.parser")
            stringBS=soup.get_text()
            searchTERM ="\"regularMarketPrice\":(.*?),\""
            marketPrice = re.search(searchTERM, stringBS).group(1)
            price = marketPrice
            data["value"] = marketPrice
            await self.send(json.dumps(data))
            await sleep(.5)