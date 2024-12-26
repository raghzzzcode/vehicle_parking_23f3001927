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
  import { ref, onMounted } from "vue";
  import Chart from "chart.js/auto";
  import AdminNavbar from "@/components/AdminNavbar.vue";
  import AppFooter from "@/components/AppFooter.vue";
  export default {
    components: {
      AdminNavbar,
      AppFooter
    },
    setup() {
      // Superficial data for the charts
      const ratingsData = ref({
        "5": 50,
        "4": 30,
        "3": 15,
        "2": 5,
        "1": 10
      });
      const serviceRequestsData = ref({
        "Received": 120,
        "Closed": 90,
        "Rejected": 15
      });
  
      onMounted(() => {
        // Prepare ratings chart data
        const ratingsChartData = [
          ratingsData.value["5"] || 0,
          ratingsData.value["4"] || 0,
          ratingsData.value["3"] || 0,
          ratingsData.value["2"] || 0,
          ratingsData.value["1"] || 0
        ];
  
        // Circle chart for Ratings
        const ctxRatings = document.getElementById("ratingsChart").getContext("2d");
        new Chart(ctxRatings, {
          type: "doughnut",
          data: {
            labels: ["⭐⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐", "⭐⭐", "⭐"],
            datasets: [
              {
                data: ratingsChartData,
                backgroundColor: ["#28a745", "#ffc107", "#fd7e14", "#e0a800", "#dc3545"],
                borderColor: "#ffffff",
                borderWidth: 3
              }
            ]
          },
          options: {
            responsive: true,
            plugins: {
              legend: {
                position: "top",
                labels: {
                  font: {
                    size: 14,
                    weight: "bold"
                  }
                }
              },
              tooltip: {
                callbacks: {
                  label: function (tooltipItem) {
                    return tooltipItem.label + ": " + tooltipItem.raw + " responses";
                  }
                }
              }
            }
          }
        });
  
        // Bar chart for Service Requests
        const ctxRequests = document.getElementById("serviceRequestsChart").getContext("2d");
        new Chart(ctxRequests, {
          type: "bar",
          data: {
            labels: ["Received", "Closed", "Rejected"],
            datasets: [
              {
                label: "Service Requests",
                data: [
                  serviceRequestsData.value["Received"] || 0,
                  serviceRequestsData.value["Closed"] || 0,
                  serviceRequestsData.value["Rejected"] || 0
                ],
                backgroundColor: ["#17a2b8", "#28a745", "#dc3545"],
                borderColor: "#ffffff",
                borderWidth: 2
              }
            ]
          },
          options: {
            responsive: true,
            scales: {
              y: {
                beginAtZero: true,
                ticks: {
                  font: {
                    size: 12,
                    weight: "bold"
                  }
                }
              },
              x: {
                ticks: {
                  font: {
                    size: 14,
                    weight: "bold"
                  }
                }
              }
            },
            plugins: {
              legend: {
                display: false
              },
              tooltip: {
                callbacks: {
                  label: function (tooltipItem) {
                    return tooltipItem.label + ": " + tooltipItem.raw;
                  }
                }
              }
            }
          }
        });
      });
  
      return {
        ratingsData,
        serviceRequestsData
      };
    }
  };
  </script>
  
  <style scoped>
  .container-fluid {
    padding: 0;
  }
  
  .card {
    margin-bottom: 20px;
  }
  </style>
  