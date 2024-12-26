<template>
    <div>
      <!-- Include Professional Navbar -->
      <ProfessionalNavbar />
  
      <div class="container-fluid mb-5">
        <div class="row">
          <!-- Left Column: Reviews/Ratings -->
          <div class="col-md-6">
            <div class="card shadow-sm border-0">
              <div class="card-body" style="min-height: 250px;">
                <h5 class="card-title" style="color: #004aad;">Reviews / Ratings</h5>
                <div class="d-flex justify-content-center">
                  <canvas id="ratingsChart" width="300" height="300"></canvas>
                </div>
              </div>
            </div>
          </div>
  
          <!-- Right Column: Service Requests -->
          <div class="col-md-6">
            <div class="card shadow-sm border-0">
              <div class="card-body" style="min-height: 250px;">
                <h5 class="card-title" style="color: #004aad;">Service Requests</h5>
                <div class="d-flex justify-content-center">
                  <canvas id="serviceRequestsChart" width="300" height="300"></canvas>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Include Footer -->
      <AppFooter />
    </div>
  </template>
  
  <script>
  import Chart from 'chart.js/auto'; 
  // Import necessary components
  import ProfessionalNavbar from '@/components/ProfessionalNavbar.vue';
  import AppFooter from '@/components/AppFooter.vue';
  
  // Dummy data for charts
  const ratingsData = { '5': 20, '4': 10, '3': 5, '2': 2, '1': 1 };
  const serviceRequestsData = { 'Received': 30, 'Closed': 25, 'Requested': 10 };
  
  export default {
    components: {
      ProfessionalNavbar,
      AppFooter
    },
    mounted() {
      this.initializeCharts();
    },
    methods: {
      initializeCharts() {
        // Prepare ratings chart data
        const ratingsChartData = [
          ratingsData['5'] || 0,
          ratingsData['4'] || 0,
          ratingsData['3'] || 0,
          ratingsData['2'] || 0,
          ratingsData['1'] || 0
        ];
  
        // Circle chart for Ratings
        const ctxRatings = document.getElementById('ratingsChart').getContext('2d');
        new Chart(ctxRatings, {
          type: 'doughnut',
          data: {
            labels: ['⭐⭐⭐⭐⭐', '⭐⭐⭐⭐', '⭐⭐⭐', '⭐⭐', '⭐'],
            datasets: [{
              data: ratingsChartData,
              backgroundColor: ['#28a745', '#ffc107', '#fd7e14', '#e0a800', '#dc3545'],
              borderColor: '#ffffff',
              borderWidth: 2
            }]
          },
          options: {
            responsive: true,
            plugins: {
              legend: { position: 'top' },
              tooltip: {
                callbacks: {
                  label: (tooltipItem) => `${tooltipItem.label}: ${tooltipItem.raw} responses`
                }
              }
            }
          }
        });
  
        // Bar chart for Service Requests
        const ctxRequests = document.getElementById('serviceRequestsChart').getContext('2d');
        new Chart(ctxRequests, {
          type: 'bar',
          data: {
            labels: ['Received', 'Closed', 'Requested'],
            datasets: [{
              label: 'Service Requests',
              data: [
                serviceRequestsData['Received'] || 0,
                serviceRequestsData['Closed'] || 0,
                serviceRequestsData['Requested'] || 0
              ],
              backgroundColor: ['#17a2b8', '#28a745', '#dc3545'],
              borderColor: '#ffffff',
              borderWidth: 2
            }]
          },
          options: {
            responsive: true,
            scales: { y: { beginAtZero: true } },
            plugins: {
              legend: { display: false },
              tooltip: {
                callbacks: {
                  label: (tooltipItem) => `${tooltipItem.label}: ${tooltipItem.raw}`
                }
              }
            }
          }
        });
      }
    }
  };
  </script>
  
  <style scoped>
  /* Add custom styling for the page */
  .card-title {
    font-size: 1.5rem;
    font-weight: bold;
  }
  
  .container-fluid {
    padding: 20px;
  }
  
  .card-body {
    background-color: #f0f8ff;
  }
  
  .card {
    border-radius: 8px;
  }
  
  .doughnut-chart,
  .bar-chart {
    max-width: 100%;
  }
  
  canvas {
    width: 100% !important;
  }
  </style>
  