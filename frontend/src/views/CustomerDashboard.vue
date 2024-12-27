<template>
  <div>
    <!-- Customer Navbar -->
    <CustomerNavbar />

    <div class="container-fluid mb-5">
      <!-- Service Options Section -->
      <h3 class="text-center mb-4" style="color: #004aad; font-weight: bold;">Looking For</h3>
      <div class="row text-center mb-5">
        <div v-for="(service, index) in services" :key="index" class="col-md-3 mb-3">
          <button type="button" class="service-btn" @click="selectService(service)">
            <p>{{ service.service_name }}</p>
          </button>
        </div>
      </div>

      <!-- Search Results and Other Sections -->
      <div v-if="searchResults.length > 0">
        <h3 class="text-center mb-4" style="color: #004aad; font-weight: bold;">Professionals</h3>
        <table class="table table-striped table-hover shadow rounded">
          <thead>
            <tr>
              <th>Professional Name</th>
              <th>Service Name</th>
              <th>Experience</th>
              <th>Address</th>
              <th>Pincode</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(result, index) in searchResults" :key="index">
              <td>{{ result.professional_name }}</td>
              <td>{{ result.service_name }}</td>
              <td>{{ result.experience }} years</td>
              <td>{{ result.address }}</td>
              <td>{{ result.pincode }}</td>
              <td>
                <button @click="bookService(result)" class="btn btn-success">Book</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else>
        <p class="text-center">Select a service to view available professionals.</p>
      </div>

      <!-- Service History Section -->
      <div class="container-fluid">
        <div class="mb-5">
          <h3 class="text-center mb-3" style="color: #004aad; font-weight: bold;">Service History</h3>
          <table class="table table-striped table-hover shadow rounded">
            <thead>
              <tr>
                <th>Service Name</th>
                <th>Professional Name</th>
                <th>Email</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(service, index) in serviceHistory" :key="index">
                <td>{{ service.service_name }}</td>
                <td>{{ service.professional_name }}</td>
                <td>{{ service.email }}</td>
                <td>
                  <button v-if="service.status !== 'Closed'" @click="closeService(service)" class="btn btn-danger">Close</button>
                  <span v-else>Closed</span>
                </td>
              </tr>
              <tr v-if="serviceHistory.length === 0">
                <td colspan="4" class="text-center">No service history.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- App Footer -->
    <AppFooter />
  </div>
</template>

<script>
import axios from "axios";
import CustomerNavbar from "@/components/CustomerNavbar.vue";
import AppFooter from "@/components/AppFooter.vue";

export default {
  name: "CustomerDashboard",
  components: {
    CustomerNavbar,
    AppFooter,
  },
  data() {
    return {
      services: [],
      searchResults: [],
      serviceHistory: [],
    };
  },
  created() {
    this.fetchServices();
    this.fetchServiceHistory();
  },
  methods: {
    // Fetch all services
    fetchServices() {
      axios.get("/api/services")
        .then((response) => {
          this.services = response.data;
        })
        .catch((error) => {
          console.error("There was an error fetching services:", error);
        });
    },
    // Fetch service history
    fetchServiceHistory() {
      axios.get("/api/service-history")
        .then((response) => {
          this.serviceHistory = response.data;
        })
        .catch((error) => {
          console.error("There was an error fetching service history:", error);
        });
    },
    // Select service and fetch professionals
    selectService(service) {
      axios.get(`/api/professionals/${service.service_id}`)
        .then((response) => {
          this.searchResults = response.data;
        })
        .catch((error) => {
          console.error("There was an error fetching professionals:", error);
        });
    },
    // Book service for a customer
    bookService(result) {
      axios.post("/api/book-service", {
        professional_id: result.professional_id,
        service_id: result.service_id,
      })
        .then(() => {
          alert(`Service booked with ${result.professional_name}`);
        })
        .catch((error) => {
          console.error("There was an error booking the service:", error);
        });
    },
    // Close a service request
    closeService(service) {
      axios.post("/api/close-service", { service_id: service.service_id })
        .then(() => {
          service.status = "Closed";
          alert(`Service for ${service.service_name} closed.`);
        })
        .catch((error) => {
          console.error("There was an error closing the service:", error);
        });
    },
  },
};
</script>

<style scoped>
/* Add your existing styles here */
</style>
