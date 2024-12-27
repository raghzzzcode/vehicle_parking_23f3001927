<template>
  <div>
    <!-- Navbar Component -->
    <CustomerNavbar />
  
    <div class="container-fluid mb-5">
      <div class="row justify-content-center">
        <!-- Right Column: Service History -->
        <div class="col-md-6">
          <div class="card shadow-lg border-0 rounded-3">
            <div class="card-body" style="min-height: 300px; padding: 30px; background: #f9f9f9;">
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
import axios from 'axios';
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
      // Initialize service history data to zero
      serviceHistoryData: {
        Requested: 0,
        Assigned: 0,
        Closed: 0
      },
      customerId: 1  // Example customer ID, this can be dynamic depending on the logged-in user
    };
  },
  mounted() {
    // Fetch the service history data from the backend
    this.fetchServiceHistory();

    // After data is fetched, create the chart
    this.createServiceHistoryChart();
  },
  methods: {
    // Fetch service history data from the backend
    fetchServiceHistory() {
      axios.get(`/api/service-history/${this.customerId}`)
        .then(response => {
          this.serviceHistoryData = response.data;
          this.createServiceHistoryChart();
        })
        .catch(error => {
          console.error("Error fetching service history:", error);
        });
    },
    
    // Create the service history chart using the fetched data
    createServiceHistoryChart() {
      const ctxHistory = document.getElementById('serviceHistoryChart').getContext('2d');
      const gradient = ctxHistory.createLinearGradient(0, 0, 0, 400);
      gradient.addColorStop(0, 'rgba(23, 162, 184, 0.6)');
      gradient.addColorStop(1, 'rgba(40, 167, 69, 0.6)');
  
      new Chart(ctxHistory, {
        type: 'bar',
        data: {
          labels: ['Requested', 'Assigned', 'Closed'],
          datasets: [
            {
              label: 'Service History',
              data: [
                this.serviceHistoryData.Requested,
                this.serviceHistoryData.Assigned,
                this.serviceHistoryData.Closed
              ],
              backgroundColor: [
                'rgba(23, 162, 184, 0.6)',
                'rgba(40, 167, 69, 0.6)',
                'rgba(255, 193, 7, 0.6)'
              ],
              borderColor: '#ffffff',
              borderWidth: 2,
              hoverBackgroundColor: [
                'rgba(0, 123, 255, 0.6)',
                'rgba(0, 255, 0, 0.6)',
                'rgba(255, 204, 0, 0.6)'
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
/* Optional: Add any custom styles you want here */
</style>
