document.addEventListener('DOMContentLoaded', function () {
  const notificationsList = document.getElementById('notifications-list');
  const notificationButton = document.getElementById('notification-button');
  let jobsData = []; // Store job data for better management

  // Function to add a notification to the dropdown list
  function addNotification(message, jobId) {
        const notificationItem = document.createElement('div');
        notificationItem.className = 'notification-item';
        notificationItem.innerHTML = `<span>${message}</span><button class="dismiss-button" data-job-id="${jobId}">×</button>`;

        // Insert the new notification at the beginning of the list
        notificationsList.insertBefore(notificationItem, notificationsList.firstChild);

        notificationsList.classList.add('show');

        notificationItem.querySelector('.dismiss-button').addEventListener('click', function () {
            const jobIdToRemove = this.getAttribute('data-job-id');
            notificationItem.remove();
        });
    }

  // Function to load job data from the table
  function loadJobsData() {
      jobsData = [];
      const jobs = document.querySelectorAll('table tbody tr');
      jobs.forEach((job, index) => {
          const companyName = job.querySelector('td:nth-child(1)').textContent;
          const jobTitle = job.querySelector('td:nth-child(2)').textContent;
          const interviewDateCell = job.querySelector('td:nth-child(5)');
          let interviewDate = null;

          if (interviewDateCell && interviewDateCell.textContent !== 'N/A') {
              interviewDate = new Date(interviewDateCell.textContent);
          }

          jobsData.push({
              id: index, // Assign a unique ID to each job
              companyName: companyName,
              jobTitle: jobTitle,
              interviewDate: interviewDate,
          });
      });
  }

  // Function to check interview dates
  function checkInterviewDates() {
      const today = new Date();
      loadJobsData(); // Reload data each time.
      jobsData.forEach((job) => {
          if (job.interviewDate) {
              const timeDifference = job.interviewDate - today;
              const daysDifference = Math.ceil(timeDifference / (1000 * 60 * 60 * 24));

              if (daysDifference === 1) {
                  const notificationMessage = `Interview Alert: ${job.jobTitle} at ${job.companyName} is comingUp!`;
                  addNotification(notificationMessage, job.id);
              }
          }
      });
  }

  // Check interview dates when the page loads
  checkInterviewDates();

  // Check interview dates periodically (e.g., every hour)
  setInterval(checkInterviewDates, 60 * 60 * 1000); // Check every hour

  // Toggle notifications dropdown
  notificationButton.addEventListener('click', function () {
      notificationsList.classList.toggle('show');
  });

  // Close notifications dropdown when clicking outside
  document.addEventListener('click', function (event) {
      if (!notificationButton.contains(event.target) && !notificationsList.contains(event.target)) {
          notificationsList.classList.remove('show');
      }
  });
});

document.addEventListener('DOMContentLoaded', function () {
    const statusSelect = document.getElementById('application_status');
    const feedbackForm = document.getElementById('feedbackFormData');
    const feedbackStatusSelect = document.getElementById('status');
    
  // Checks the status of application to be one of the Offer Received or Rejected, before the feedback form is populated
    function toggleFeedbackOption() {
      if (statusSelect.value === 'Rejected' || statusSelect.value === 'Offer Received') {
        feedbackForm.style.display = 'block';
        feedbackStatusSelect.value = statusSelect.value;
      } else {
        feedbackForm.style.display = 'none';
      }
    }
    toggleFeedbackOption();
    statusSelect.addEventListener('change', toggleFeedbackOption);
  });

  document.getElementById('sortPriority').addEventListener('click', function() {
    fetch('/sort_jobs')
        .then(response => response.json())
        .then(data => {
            const tableBody = document.getElementById('jobTable');
            tableBody.innerHTML = ''; // Clear the table

            data.forEach(job => {
                const row = document.createElement('tr');
                let priorityList = '';
                if (job[8] === 3) {
                    priorityList = '★★★';
                } else if (job[8] === 2) {
                    priorityList = '★★';
                } else if (job[8] === 1) {
                    priorityList = '★';
                } else {
                    priorityList = 'Error';
                }

                row.innerHTML = `
                    <td>${priorityList}</td>
                    <td>${job[1]}</td>
                    <td>${job[2]}</td>
                    <td>${job[3]}</td>
                    <td>${job[4]}</td>
                    <td>${job[5] || 'N/A'}</td>
                    <td>${job[6] || 'N/A'}</td>
                    <td>${job[7] || 'N/A'}</td>
                    <td>
                      <a href="/edit/${job[0]}">Edit</a> 
                      <a href="/delete/${job[0]}">Delete</a>
                    </td>
                    <td>${job[3] === "Rejected" || job[3] === "Offer Received" ? `<a href="/feedback/${job[0]}">Notes</a>` : ''}</td>
                `;
                tableBody.appendChild(row);
            });
        });
});

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
