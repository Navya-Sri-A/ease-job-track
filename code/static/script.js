document.addEventListener('DOMContentLoaded', function () {
  const darkModeToggle = document.getElementById('dark-mode-toggle');
  const body = document.body;

  // Check local storage for dark mode preference
  const isDarkMode = localStorage.getItem('darkMode') === 'true';
  console.log('Dark Mode Preference:', isDarkMode); // Debugging line

  // Apply dark mode if it was enabled
  if (isDarkMode) {
    body.classList.add('dark-mode');
    if (darkModeToggle) {
      darkModeToggle.innerHTML = '<i class="fas fa-sun"></i> Light Mode';
    }
  }

  // Toggle dark mode (only if the button exists)
  if (darkModeToggle) {
    darkModeToggle.addEventListener('click', function () {
      console.log('Dark mode toggle clicked'); // Debugging line
      body.classList.toggle('dark-mode');
      const isDarkMode = body.classList.contains('dark-mode');
      localStorage.setItem('darkMode', isDarkMode);

      // Update button text
      if (isDarkMode) {
        darkModeToggle.innerHTML = '<i class="fas fa-sun"></i> Light Mode';
      } else {
        darkModeToggle.innerHTML = '<i class="fas fa-moon"></i> Dark Mode';
      }
    });
  }
});

  // Only run chart-related code if the elements exist
  const statusLabelsElement = document.getElementById('statusLabels');
  const statusCountsElement = document.getElementById('statusCounts');
  const companyNamesElement = document.getElementById('companyNames');
  const companyCountsElement = document.getElementById('companyCounts');

  if (statusLabelsElement && statusCountsElement && companyNamesElement && companyCountsElement) {
    // Pie Chart Data
    const statusLabels = JSON.parse(statusLabelsElement.textContent);
    const statusCounts = JSON.parse(statusCountsElement.textContent);

    // Map statuses to colors
    const statusColorMap = {
      Applied: "#FFCE56", // Yellow
      "Interview Scheduled": "#36A2EB", // Blue
      Rejected: "#FF6384", // Red
      "Offer Received": "#4BC0C0", // Teal
    };

    const backgroundColor = statusLabels.map((label) => statusColorMap[label]);

    // Create the Pie Chart
    let pieChart;
    const pieCtx = document.getElementById('statusChart').getContext('2d');
    function createPieChart() {
      pieChart = new Chart(pieCtx, {
        type: "pie",
        data: {
          labels: statusLabels,
          datasets: [
            {
              data: statusCounts,
              backgroundColor: backgroundColor,
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: "top",
            },
            title: {
              display: true,
            },
          },
        },
      });
    }

    // Bar Chart Data
    const companyNames = JSON.parse(companyNamesElement.textContent);
    const companyCounts = JSON.parse(companyCountsElement.textContent);

    // Create the Bar Chart
    let barChart;
    const barCtx = document.getElementById('companyChart').getContext('2d');
    function createBarChart() {
      barChart = new Chart(barCtx, {
        type: "bar",
        data: {
          labels: companyNames,
          datasets: [
            {
              label: "Number of Applications",
              data: companyCounts,
              backgroundColor: "#007bff",
              borderColor: "#0056b3",
              borderWidth: 1,
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              display: false,
            },
            title: {
              display: true,
              text: "Applications per Company",
            },
          },
          scales: {
            y: {
              beginAtZero: true,
              title: {
                display: true,
                text: "Number of Applications",
              },
              ticks: {
                stepSize: 1,
                precision: 0,
              },
            },
            x: {
              title: {
                display: true,
                text: "Company",
              },
            },
          },
        },
      });
    }

    // Referencing to the pop-up, buttons and tabs
    const visualizePopup = document.getElementById('visualizePopup');
    const visualizeButton = document.getElementById('visualizeButton');
    const closeVisualize = document.getElementById('closeVisualize');
    const pieTabButton = document.getElementById('pieTabButton');
    const barTabButton = document.getElementById('barTabButton');
    const pieChartContainer = document.getElementById('pieChartContainer');
    const barChartContainer = document.getElementById('barChartContainer');

    // Visualizing pop-up when the Visualize button is clicked
    if (visualizeButton) {
      visualizeButton.addEventListener("click", () => {
        visualizePopup.style.display = "flex";
        if (!pieChart) {
          createPieChart();
        }
      });
    }

    if (closeVisualize) {
      closeVisualize.addEventListener("click", () => {
        visualizePopup.style.display = "none";
      });
    }

    // Switching to Pie Chart tab
    if (pieTabButton) {
      pieTabButton.addEventListener("click", () => {
        pieTabButton.classList.add("active");
        barTabButton.classList.remove("active");
        pieChartContainer.classList.add("active");
        barChartContainer.classList.remove("active");
        if (!pieChart) {
          createPieChart();
        } else {
          pieChart.update();
        }
      });
    }

    // Switching to Bar Chart tab
    if (barTabButton) {
      barTabButton.addEventListener("click", () => {
        barTabButton.classList.add("active");
        pieTabButton.classList.remove("active");
        barChartContainer.classList.add("active");
        pieChartContainer.classList.remove("active");
        if (!barChart) {
          createBarChart();
        } else {
          barChart.update();
        }
      });
    }

    // Hiding the pop-up when clicked outside of it
    window.addEventListener("click", (event) => {
      if (event.target === visualizePopup) {
        visualizePopup.style.display = "none";
      }
    });
  }
