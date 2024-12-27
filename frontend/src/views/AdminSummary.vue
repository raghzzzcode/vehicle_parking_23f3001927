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
import axios from "axios";
import AdminNavbar from "@/components/AdminNavbar.vue";
import AppFooter from "@/components/AppFooter.vue";

export default {
  components: {
    AdminNavbar,
    AppFooter
  },
  setup() {
    const ratingsData = ref({});
    const serviceRequestsData = ref({});

    const fetchRatingsData = async () => {
      try {
        const response = await axios.get("/api/reviews/ratings-summary");
        ratingsData.value = response.data; // Assumes response format matches { "5": x, "4": y, ... }
      } catch (error) {
        console.error("Error fetching ratings data:", error);
      }
    };

    const fetchServiceRequestsData = async () => {
      try {
        const response = await axios.get("/api/requests/service-summary");
        serviceRequestsData.value = response.data; // Assumes response format matches { "Received": x, ... }
      } catch (error) {
        console.error("Error fetching service requests data:", error);
      }
    };

    const initializeCharts = () => {
      const ratingsChartData = [
        ratingsData.value["5"] || 0,
        ratingsData.value["4"] || 0,
        ratingsData.value["3"] || 0,
        ratingsData.value["2"] || 0,
        ratingsData.value["1"] || 0
      ];

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

      const serviceRequestsChartData = [
        serviceRequestsData.value["Received"] || 0,
        serviceRequestsData.value["Closed"] || 0,
        serviceRequestsData.value["Rejected"] || 0
      ];

      const ctxRequests = document.getElementById("serviceRequestsChart").getContext("2d");
      new Chart(ctxRequests, {
        type: "bar",
        data: {
          labels: ["Received", "Closed", "Rejected"],
          datasets: [
            {
              label: "Service Requests",
              data: serviceRequestsChartData,
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
    };

    onMounted(async () => {
      await Promise.all([fetchRatingsData(), fetchServiceRequestsData()]);
      initializeCharts();
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
