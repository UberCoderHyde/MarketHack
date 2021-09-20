const stock = JSON.parse(document.getElementById('stock').textContent);
var link = "https://query1.finance.yahoo.com/v7/finance/quote?lang=en-US&region=US&corsDomain=finance.yahoo.com&symbols="+stock
var socket = new WebSocket('ws://localhost:8000/ws/stock/'+stock+'/');
socket.onmessage = function(e){
    var djangoData = JSON.parse(e.data);
    console.log(djangoData);
    document.querySelector('#PE').innerText = "Price to Equity:  "+djangoData.PE;
    document.querySelector('#PriceToBook').innerText = "Price To Book: "+djangoData.PriceToBook;
    document.querySelector('#DE').innerText = "Debt To Equity: "+djangoData.DE;
    document.querySelector('#FCF').innerText = "Free Cash Flow: "+djangoData.FCF;
    document.querySelector('#PEG').innerText = "Price Earnings To Growth: "+djangoData.PEG;

    document.querySelector('#price').innerText = "Live Price = "+djangoData.value;
}