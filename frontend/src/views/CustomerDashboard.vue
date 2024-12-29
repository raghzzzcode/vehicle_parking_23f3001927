<template>
  <div>
    <!-- Customer Navbar -->
    <CustomerNavbar />

    <div class="container-fluid mb-5">
      <!-- Service Options Section -->
      <h3 class="text-center mb-4" style="color: #004aad; font-weight: bold;">Looking For</h3>
      <div class="row text-center mb-5">
        <div v-for="service in services" :key="service.id" class="col-md-3 mb-3">
          <button type="button" class="service-btn" @click="selectService(service.id)">
            <p>{{ service.name }}</p>
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
            <tr v-for="result in searchResults" :key="result.professional_id">
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
  <tr v-for="service in serviceHistory" :key="service.id">
    <td>{{ service.service_name }}</td>
    <td>{{ service.professional_name }}</td>
    <td>{{ service.email }}</td>
    <td>
      <!-- Only show 'Close' button if the status is not 'Completed' -->
      <button v-if="service.status !== 'completed'" @click="closeService(service.id)" class="btn btn-danger">Close</button>
      <!-- Show 'Closed' if the status is 'Completed' -->
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
import instance from "@/axios.js";
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
  methods: {
    async fetchServices() {
      try {
        const response = await instance.get("get_services");
        this.services = response.data;
      } catch (error) {
        console.error("Error fetching services:", error);
      }
    },
    async selectService(serviceId) {
      try {
        const response = await instance.get(`get_professional/${serviceId}`);
        this.searchResults = response.data;
      } catch (error) {
        console.error("Error fetching professionals:", error);
      }
    },
    async bookService(result) {
      try {
        const customer_email = this.getCustomerEmail(); // Fetch customer ID dynamically
        const response = await instance.post("book-service", {
          service_id: result.service_id,
          customer_email: customer_email,
          professional_id: result.professional_id,
        });
        alert(response.data.message);
        this.fetchServiceHistory();
      } catch (error) {
        console.error("Error booking service:", error);
      }
    },
    async closeService() {
  try {
    const customer_email= this.getCustomerEmail(); // Fetch customer ID dynamically
    const professional_email = this.getProfessionalEmail(); // Fetch professional ID dynamically
    const response = await instance.post("close-service", {
      customer_email: customer_email,
      professional_email: professional_email,
    });
    
    alert(response.data.message);
    this.$router.push({
      path: "/customer_remarks",
      query: {
        customer_email: customer_email,
        professional_email: professional_email,
        request_id: response.data.request_id,
        service_name: response.data.service_name,
        professional_name: response.data.professional_name,
      }
    });
    
  } catch (error) {
    console.error("Error closing service:", error);
  }
},
    async fetchServiceHistory() {
      try {
        const customerEmail = this.getCustomerEmail(); // Fetch customer ID dynamically
        const response = await instance.get(`get_service_history?customer_email=${customerEmail}`);
        this.serviceHistory = response.data;
      } catch (error) {
        console.error("Error fetching service history:", error);
      }
    },
    getCustomerEmail() {
      // Fetch customer ID from session, token, or another dynamic source
      return localStorage.getItem("customer_email");
    },
    getProfessionalEmail() {
      // Fetch professional ID from session, token, or another dynamic source
      return localStorage.getItem("professional_email");
    },
  },
  async mounted() {
    await this.fetchServices();
    await this.fetchServiceHistory();
  },
};
</script>

<style scoped>
/* Styling remains unchanged */
.service-btn {
  display: block;
  background-color: #007bff;
  color: white;
  border: none;
  padding: 12px 24px;
  font-size: 16px;
  border-radius: 8px;
  width: 100%;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
}

.service-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
}

.service-btn p {
  margin: 0;
}

.table {
  background-color: #ffffff;
  border-radius: 10px;
}

.table th,
.table td {
  text-align: center;
  padding: 15px;
}

.table-striped tbody tr:nth-of-type(odd) {
  background-color: #f9f9f9;
}

.table-hover tbody tr:hover {
  background-color: #f1f1f1;
}

.btn-success {
  background-color: #28a745;
  color: white;
  border-radius: 5px;
  padding: 8px 16px;
  transition: background-color 0.3s;
}

.btn-success:hover {
  background-color: #218838;
}

.btn-danger {
  background-color: #dc3545;
  color: white;
  border-radius: 5px;
  padding: 8px 16px;
  transition: background-color 0.3s;
}

.btn-danger:hover {
  background-color: #c82333;
}
</style>