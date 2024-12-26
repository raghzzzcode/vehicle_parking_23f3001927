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
  // Importing the Chart.js library
  import Chart from 'chart.js/auto';  // This will automatically import everything needed for Chart.js
  
    // Importing the CustomerNavbar and AppFooter components
    import CustomerNavbar from "@/components/CustomerNavbar.vue";
    import AppFooter from "@/components/AppFooter.vue";
  
  export default {
    components: {
      CustomerNavbar,
      AppFooter
    },
    data() {
      return {
        // Sample static data for the service history chart
        serviceHistoryData: {
          Requested: 3,
          Closed: 5,
          Assigned: 2
        }
      };
    },
    mounted() {
      // Bar chart for Service History
      const ctxHistory = document.getElementById('serviceHistoryChart').getContext('2d');
      const gradient = ctxHistory.createLinearGradient(0, 0, 0, 400);
      gradient.addColorStop(0, 'rgba(23, 162, 184, 0.6)');
      gradient.addColorStop(1, 'rgba(40, 167, 69, 0.6)');
  
      new Chart(ctxHistory, {
        type: 'bar',
        data: {
          labels: ['Requested', 'Closed', 'Assigned'],
          datasets: [
            {
              label: 'Service History',
              data: [
                this.serviceHistoryData.Requested || 0,
                this.serviceHistoryData.Closed || 0,
                this.serviceHistoryData.Assigned || 0
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
              display: false // Hide legend as the chart already includes labels for each bar
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
  };
  </script>
  
  <style scoped>
  /* Optional: Add any custom styles you want here */
  </style>
  