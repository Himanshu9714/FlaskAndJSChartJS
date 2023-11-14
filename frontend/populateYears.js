// Function to populate the years dropdown
function populateYears(elmId, yearsList) {

    // Get the year selector element
    const yearSelector = document.getElementById(elmId);

    // Populate the dropdown list with the years from the array
    yearsList.forEach(year => {
        const option = document.createElement('option');
        option.value = year;
        option.textContent = year;
        yearSelector.appendChild(option);
    });
}

// API endpoint for the years API
YEARS_API = `${API_URL}/get-years-values`
fetch(YEARS_API)
    .then(response => response.json())
    .then(data => {

        // Get the years list from the years key
        yearsList = data.years

        // Populate the dropdowns
        populateYears("yearSelector1", yearsList)
        populateYears("yearSelector2", yearsList)
    })