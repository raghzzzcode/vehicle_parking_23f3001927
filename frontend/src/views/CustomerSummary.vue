<template>
  <div>
    <!-- Navbar Component -->
    <CustomerNavbar />
  
    <div class="container-fluid mb-5">
      <div class="row justify-content-center">
        <!-- Right Column: Service History -->
        <div class="col-md-6">
          <div class="card shadow-lg border-0 rounded-3">
            <div class="card-body" style="min-height: 350px; padding: 30px; background: #f9f9f9;">
              <h5 class="card-title text-center" style="color: #004aad; font-weight: 700; font-size: 1.7rem;">
                Service History
              </h5>
              <div class="d-flex justify-content-center my-4">
                <canvas id="serviceHistoryChart" width="350" height="350"></canvas>
              </div>
              <p class="text-center" style="font-size: 1.1rem; color: #555;">
                Track and monitor the status of your service requests.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  
    <!-- Footer Component -->
    <AppFooter />
  </div>
</template>

<script>
// Importing the necessary libraries
import instance from '@/axios.js';
import Chart from 'chart.js/auto';
import CustomerNavbar from "@/components/CustomerNavbar.vue";
import AppFooter from "@/components/AppFooter.vue";

export default {
  components: {
    CustomerNavbar,
    AppFooter
  },
  data() {
    return {
      serviceHistoryData: {
        Requested: 0,
        Assigned: 0,
        Closed: 0,
        Rejected: 0
      },
      customerEmail: localStorage.getItem('customer_email')
    };
  },
  mounted() {
    this.fetchServiceHistory();
    this.createServiceHistoryChart();
  },
  methods: {
    fetchServiceHistory() {
      instance.get(`service-history/${this.customerEmail}`)
        .then(response => {
          this.serviceHistoryData = response.data;
          this.createServiceHistoryChart();
          console.log(response.data);
        })
        .catch(error => {
          console.error("Error fetching service history:", error);
        });
    },
    
    createServiceHistoryChart() {
  const ctxHistory = document.getElementById('serviceHistoryChart').getContext('2d');

  // Check if there's an existing chart and destroy it
  if (this.chartInstance) {
    this.chartInstance.destroy();
  }

  // Create a new gradient for the chart background
  const gradient = ctxHistory.createLinearGradient(0, 0, 0, 400);
  gradient.addColorStop(0, 'rgba(23, 162, 184, 0.6)');
  gradient.addColorStop(1, 'rgba(40, 167, 69, 0.6)');

  // Create the new chart instance with the "Rejected" bar added
  this.chartInstance = new Chart(ctxHistory, {
    type: 'bar',
    data: {
      labels: ['Requested', 'Assigned', 'Closed', 'Rejected'], // Add "Rejected" to the labels
      datasets: [
        {
          label: 'Service History',
          data: [
            this.serviceHistoryData.Requested,
            this.serviceHistoryData.Assigned,
            this.serviceHistoryData.Closed,
            this.serviceHistoryData.Rejected // Add the "Rejected" data
          ],
          backgroundColor: [
            'rgba(23, 162, 184, 0.6)',
            'rgba(40, 167, 69, 0.6)',
            'rgba(255, 193, 7, 0.6)',
            'rgba(255, 0, 0, 0.6)' // Add a color for the "Rejected" bar
          ],
          borderColor: '#ffffff',
          borderWidth: 2,
          hoverBackgroundColor: [
            'rgba(0, 123, 255, 0.6)',
            'rgba(0, 255, 0, 0.6)',
            'rgba(255, 204, 0, 0.6)',
            'rgba(255, 0, 0, 0.6)' // Add a hover color for the "Rejected" bar
          ],
          hoverBorderColor: '#ffffff',
          hoverBorderWidth: 3
        }
      ]
    },
    options: {
      responsive: true,
      scales: {
        y: {
          beginAtZero: true,
          ticks: {
            stepSize: 1,
            font: {
              size: 14,
              weight: 'bold',
              family: 'Arial, sans-serif'
            }
          }
        },
        x: {
          ticks: {
            font: {
              size: 14,
              weight: 'bold',
              family: 'Arial, sans-serif'
            }
          }
        }
      },
      plugins: {
        legend: {
          display: false
        },
        tooltip: {
          backgroundColor: '#004aad',
          titleFont: {
            size: 14,
            weight: 'bold'
          },
          bodyFont: {
            size: 12
          },
          callbacks: {
            label: function (tooltipItem) {
              return tooltipItem.label + ': ' + tooltipItem.raw;
            }
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
/* Optional: Custom styles for centering and card layout */
.card-body {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.container-fluid {
  max-width: 1200px;
  margin: 0 auto;
}

h5.card-title {
  margin-bottom: 30px;
}

canvas {
  max-width: 100%;
  height: auto;
}
</style>
