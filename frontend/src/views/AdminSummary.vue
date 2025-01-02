<template>
  <div class="container-fluid mb-5">
    <AdminNavbar />
    <div class="row">
      <!-- Left Column: Reviews/Ratings -->
      <div class="col-md-6">
        <div class="card shadow-lg border-0 rounded-3">
          <div class="card-body" style="min-height: 250px; padding: 1.5rem;">
            <h5 class="card-title mb-4" style="color: #004aad; font-weight: 600;">Reviews / Ratings</h5>
            <div class="d-flex justify-content-center">
              <canvas id="ratingsChart" width="300" height="300"></canvas>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Column: Service Requests -->
      <div class="col-md-6">
        <div class="card shadow-lg border-0 rounded-3">
          <div class="card-body" style="min-height: 250px; padding: 1.5rem;">
            <h5 class="card-title mb-4" style="color: #004aad; font-weight: 600;">Service Requests</h5>
            <div class="d-flex justify-content-center">
              <canvas id="serviceRequestsChart" width="300" height="300"></canvas>
            </div>
          </div>
        </div>
      </div>
    </div>
    <AppFooter />
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import Chart from 'chart.js/auto';
import instance from '@/axios.js';
import AdminNavbar from '@/components/AdminNavbar.vue';
import AppFooter from '@/components/AppFooter.vue';

export default {
  components: {
    AdminNavbar,
    AppFooter,
  },
  setup() {
    const ratingsData = ref({});
    const serviceRequestsData = ref({});

    // Fetch ratings data from API
    const fetchRatingsData = async () => {
      try {
        const response = await instance.get('ratings-summary'); // Ensure this matches your backend route
        ratingsData.value = response.data; // Assumes response format matches { "5": x, "4": y, ... }
      } catch (error) {
        console.error('Error fetching ratings data:', error);
      }
    };

    // Fetch service requests data from API
    const fetchServiceRequestsData = async () => {
      try {
        const response = await instance.get('service-summary'); // Ensure this matches your backend route
        console.log(response.data);
        serviceRequestsData.value = response.data; // Assumes response format matches { "Received": x, ... }
      } catch (error) {
        console.error('Error fetching service requests data:', error);
      }
    };

    // Initialize the charts
    const initializeCharts = () => {
      // Ratings Doughnut Chart
      const ratingsChartData = [
        ratingsData.value['5'] || 0,
        ratingsData.value['4'] || 0,
        ratingsData.value['3'] || 0,
        ratingsData.value['2'] || 0,
        ratingsData.value['1'] || 0,
      ];

      const ctxRatings = document.getElementById('ratingsChart').getContext('2d');
      new Chart(ctxRatings, {
        type: 'doughnut',
        data: {
          labels: ['⭐⭐⭐⭐⭐', '⭐⭐⭐⭐', '⭐⭐⭐', '⭐⭐', '⭐'],
          datasets: [
            {
              data: ratingsChartData,
              backgroundColor: ['#28a745', '#ffc107', '#fd7e14', '#e0a800', '#dc3545'],
              borderColor: '#ffffff',
              borderWidth: 3,
            },
          ],
        },
        options: {
          responsive: true,
          plugins: {
            legend: {
              position: 'top',
              labels: {
                font: {
                  size: 14,
                  weight: 'bold',
                },
              },
            },
            tooltip: {
              callbacks: {
                label: (tooltipItem) => `${tooltipItem.label}: ${tooltipItem.raw} responses`,
              },
            },
          },
        },
      });

      // Service Requests Bar Chart
      const serviceRequestsChartData = [
        serviceRequestsData.value['Requested'] || 0,
        serviceRequestsData.value['Completed'] || 0,
        serviceRequestsData.value['Rejected'] || 0,
        serviceRequestsData.value['Assigned'] || 0, // Added Assigned bar
      ];

      const ctxRequests = document.getElementById('serviceRequestsChart').getContext('2d');
      new Chart(ctxRequests, {
        type: 'bar',
        data: {
          labels: ['Received', 'Closed', 'Rejected', 'Assigned'], // Added Assigned label
          datasets: [
            {
              label: 'Service Requests',
              data: serviceRequestsChartData,
              backgroundColor: ['#17a2b8', '#28a745', '#dc3545', '#ffc107'], // Added color for Assigned
              borderColor: '#ffffff',
              borderWidth: 2,
            },
          ],
        },
        options: {
          responsive: true,
          scales: {
            y: {
              beginAtZero: true,
              ticks: {
                font: {
                  size: 12,
                  weight: 'bold',
                },
              },
            },
            x: {
              ticks: {
                font: {
                  size: 14,
                  weight: 'bold',
                },
              },
            },
          },
          plugins: {
            legend: {
              display: false,
            },
            tooltip: {
              callbacks: {
                label: (tooltipItem) => `${tooltipItem.label}: ${tooltipItem.raw}`,
              },
            },
          },
        },
      });
    };

    // Fetch data and initialize charts on mount
    onMounted(async () => {
      await Promise.all([fetchRatingsData(), fetchServiceRequestsData()]);
      initializeCharts();
    });

    return {
      ratingsData,
      serviceRequestsData,
    };
  },
};
</script>

<style scoped>
.container-fluid {
  padding: 0;
}

.card {
  margin-bottom: 20px;
}

.card-body {
  background-color: #f8f9fa;
}

.card-title {
  font-size: 1.5rem;
}

canvas {
  width: 100% !important;
}
</style>
