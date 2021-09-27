var today = new Date();
const stock = JSON.parse(document.getElementById('stock').textContent);
var ctx = document.getElementById('myChart').getContext('2d');
var graphData = {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Live Price',
            data: [],
            backgroundColor: [
                'rgba(73, 198, 230, 1)',
            ],
            borderWidth: 1
        }]
    },
    options: {
    }
};
var chartMaxItems = 15;
var myChart = new Chart(ctx, graphData);
var socket = new WebSocket('ws://localhost:8000/ws/stock/'+stock+'/');
socket.onmessage = function(e){
    var djangoData = JSON.parse(e.data);
    if(graphData.data.labels.length <= chartMaxItems){
        var newGraphData = graphData.data.datasets[0].data;
        newGraphData.push(djangoData.value);
        graphData.data.labels.push(today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds());
        graphData.data.datasets[0].data = newGraphData;
        myChart.update();
    }
    else{
        graphData.data.labels.shift();
        graphData.data.datasets[0].data.shift();
        var newGraphData = graphData.data.datasets[0].data;
        newGraphData.push(djangoData.value);
        graphData.data.labels.push(today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds());
        graphData.data.datasets[0].data = newGraphData;
        myChart.update();
    }
    
    document.querySelector('#PE').innerText = "Price to Equity:  "+djangoData.PE;
    document.querySelector('#PriceToBook').innerText = "Price To Book: "+djangoData.PriceToBook;
    document.querySelector('#DE').innerText = "Debt To Equity: "+djangoData.DE;
    document.querySelector('#FCF').innerText = "Free Cash Flow: "+djangoData.FCF;
    document.querySelector('#PEG').innerText = "Price Earnings To Growth: "+djangoData.PEG;

    document.querySelector('#price').innerText = "Live Price = "+djangoData.value;
}