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
import instance from '@/axios.js'; // Import the Axios instance
import Chart from 'chart.js/auto'; 
import ProfessionalNavbar from '@/components/ProfessionalNavbar.vue';
import AppFooter from '@/components/AppFooter.vue';

export default {
  components: {
    ProfessionalNavbar,
    AppFooter
  },
  data() {
    return {
      ratingsData: {}, // For storing ratings data
      serviceRequestsData: {}, // For storing service requests data
      professionalEmail: localStorage.getItem('professional_email')
    };
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      try {
        // Fetch ratings data from the Flask API with the professional's email
        const reviewsResponse = await instance.get('professional/reviews-ratings', {
          params: { email: this.professionalEmail }
        });
        const { ratingsData } = reviewsResponse.data;
        this.ratingsData = ratingsData;

        // Fetch service requests data from the Flask API with the professional's email
        const serviceRequestsResponse = await instance.get('professional/service-requests', {
          params: { email: this.professionalEmail }
        });
        const { serviceRequestsData } = serviceRequestsResponse.data;
        this.serviceRequestsData = serviceRequestsData;
        
        console.log('Ratings Data:', this.ratingsData);
        console.log('Service Requests Data:', this.serviceRequestsData);

        // Initialize the charts after data is fetched
        this.initializeCharts();
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    },
    initializeCharts() {
      // Destroy the existing ratings chart if it exists
      if (this.ratingsChartInstance) {
        this.ratingsChartInstance.destroy();
      }

      // Prepare ratings chart data
      const ratingsChartData = [
        this.ratingsData['5'] || 0,
        this.ratingsData['4'] || 0,
        this.ratingsData['3'] || 0,
        this.ratingsData['2'] || 0,
        this.ratingsData['1'] || 0
      ];

      // Circle chart for Ratings
      const ctxRatings = document.getElementById('ratingsChart').getContext('2d');
      this.ratingsChartInstance = new Chart(ctxRatings, {
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

      // Destroy the existing service requests chart if it exists
      if (this.serviceRequestsChartInstance) {
        this.serviceRequestsChartInstance.destroy();
      }

      // Prepare service requests data
      const serviceRequestsData = [
        this.serviceRequestsData['Received'] || 0,
        this.serviceRequestsData['Closed'] || 0,
        this.serviceRequestsData['Requested'] || 0,
        this.serviceRequestsData['Assigned'] || 0,
        this.serviceRequestsData['Rejected'] || 0
      ];

      // Bar chart for Service Requests
      const ctxRequests = document.getElementById('serviceRequestsChart').getContext('2d');
      this.serviceRequestsChartInstance = new Chart(ctxRequests, {
        type: 'bar',
        data: {
          labels: ['Received', 'Closed', 'Requested', 'Assigned', 'Rejected'],
          datasets: [{
            label: 'Service Requests',
            data: serviceRequestsData,
            backgroundColor: ['#17a2b8', '#28a745', '#dc3545', '#ffc107', '#fd7e14'],
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
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.doughnut-chart,
.bar-chart {
  max-width: 100%;
}

canvas {
  width: 100% !important;
}
</style>
