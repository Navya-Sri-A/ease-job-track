// Pie Chart Data
const statusLabels = JSON.parse(
  document.getElementById("statusLabels").textContent
);
const statusCounts = JSON.parse(
  document.getElementById("statusCounts").textContent
);

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
const pieCtx = document.getElementById("statusChart").getContext("2d");
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
const companyNames = JSON.parse(
  document.getElementById("companyNames").textContent
);
const companyCounts = JSON.parse(
  document.getElementById("companyCounts").textContent
);

// Create the Bar Chart
let barChart;
const barCtx = document.getElementById("companyChart").getContext("2d");
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
const visualizePopup = document.getElementById("visualizePopup");
const visualizeButton = document.getElementById("visualizeButton");
const closeVisualize = document.getElementById("closeVisualize");
const pieTabButton = document.getElementById("pieTabButton");
const barTabButton = document.getElementById("barTabButton");
const pieChartContainer = document.getElementById("pieChartContainer");
const barChartContainer = document.getElementById("barChartContainer");

// Visualizing pop-up when the Visualize button is clicked
visualizeButton.addEventListener("click", () => {
  visualizePopup.style.display = "flex";
  if (!pieChart) {
    createPieChart();
  }
});

closeVisualize.addEventListener("click", () => {
  visualizePopup.style.display = "none";
});

// Switching to Pie Chart tab
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

// Switching to Bar Chart tab
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

// Hiding the pop-up when clicked outside of it
window.addEventListener("click", (event) => {
  if (event.target === visualizePopup) {
    visualizePopup.style.display = "none";
  }
});
