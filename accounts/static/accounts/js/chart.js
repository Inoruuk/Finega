function renderChart(data, labels) {
    var ctx = document.getElementById("myChart").getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'This week',
                data: data,
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
            },
            {
                label: 'End week',
                data: data2,
                borderColor: 'rgba(75, 75, 192, 1)',
                backgroundColor: 'rgba(75, 75, 192, 0.2)',
            },
            {
                label: 'Last week',
                data: data3,
                borderColor: 'rgba(75, 192, 75, 1)',
                backgroundColor: 'rgba(75, 192, 75, 0.2)',
            }]
        },
    });
}

$("#renderBtn").click(
    function () {
        data = ["0", "14", "2", "15", "18", "19", "22"];
        data2 = [0, 0, 10, 10, 10, 0];
        data3 = [2, 4, 8, 16, 32, 64, 28];
        labels =  ["Alexandre", "Louis", "Sebastien", "Pilippe", "Porticia", "Bernanouille"];
        renderChart(data, labels, data2, labels, data3, labels);
    }
);