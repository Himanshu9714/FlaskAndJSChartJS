function showBar() {

    // API endpoint for the bar
    STATS_API = `${API_URL}/get-stats`

    // Get the user selected values
    let year1 = document.getElementById("yearSelector1").value;
    let year2 = document.getElementById("yearSelector2").value;

    // Create a payload for the filters
    const filters = {
        "start_year": year1 > year2 ? year2 : year1,
        "end_year": year1 < year2 ? year2 : year1,
    }

    // Hit the API
    fetch(STATS_API, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(filters) // Passing payload
    })
        .then(response => response.json())
        .then(apiResponse => {

            // Get the xaxis values from the object key
            let labels = Object.keys(apiResponse)

            // Get the statistics data from the values
            let data = Object.values(apiResponse)

            // Store the each key separately for bar line
            let intensityData = data.map(item => item.intensity);
            let likelihoodData = data.map(item => item.likelihood);
            let relevanceData = data.map(item => item.relevance);

            // Create a bar chart
            var ctx = document.getElementById('myChart').getContext('2d');
            var myChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: labels, // Xaxis calues
                    datasets: [
                        {
                            label: 'Intensity',
                            data: intensityData,
                            backgroundColor: 'rgba(255, 99, 132, 0.5)', // Red color
                        },
                        {
                            label: 'Likelihood',
                            data: likelihoodData,
                            backgroundColor: 'rgba(54, 162, 235, 0.5)', // Blue color
                        },
                        {
                            label: 'Relevance',
                            data: relevanceData,
                            backgroundColor: 'rgba(255, 206, 86, 0.5)', // Yellow color
                        },
                    ]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        })
        .catch(error => console.error('Error fetching data:', error));
}


function showPie() {

    // API endpoint for the pie chart
    COUNTS_API = `${API_URL}/get-counts`;

    // Get the user selected values
    let year1 = document.getElementById("yearSelector1").value;
    let year2 = document.getElementById("yearSelector2").value;
    let groupBy = document.getElementById("groupby").value;

    // If group by is not selected, fall back to default value
    groupBy = groupBy ? groupBy : "country";

    // Payload for the API
    const payload = {
        "start_year": year1 > year2 ? year2 : year1,
        "end_year": year1 < year2 ? year2 : year1,
        "group_by": groupBy
    }

    // Hit the API
    fetch(COUNTS_API, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
    })
        .then(response => response.json())
        .then(apiResponse => {
            var ctx = document.getElementById('countryChart').getContext('2d');

            // Function to generate an array of random colors
            function generateRandomColors(count) {

                // Generate `count` number of colors to show on the pie chart
                const colors = [];
                for (let i = 0; i < count; i++) {
                    const randomColor = `rgba(${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, ${Math.floor(Math.random() * 256)}, 0.5)`;
                    colors.push(randomColor);
                }
                return colors;
            }

            // Number of legends for the chart
            const legendCount = apiResponse.xaxis.length;

            // Display the pie chart
            var countryChart = new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: apiResponse.xaxis,
                    datasets: [
                        {
                            data: apiResponse.yaxis,
                            backgroundColor: generateRandomColors(legendCount),
                        },
                    ]
                },
            });
        })
        .catch(error => console.error('Error fetching data:', error));
}

function showChart() {
    // Function to show the bar and pie charts
    let instances = Chart.instances;

    // Remove any Chart instances before creating the new one
    for (idx in instances) {
        instances[idx].destroy();
    }

    // Show bar and pie chart
    showBar()
    showPie()
}