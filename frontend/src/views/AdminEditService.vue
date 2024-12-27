<template>
  <div>
    <!-- Admin Navbar -->
    <AdminNavbar />

    <!-- Edit Service Section -->
    <div class="container-fluid mb-5">
      <h3 class="text-center mb-4" style="color: #004aad;">Edit Service</h3>

      <!-- Edit Service Form -->
      <form @submit.prevent="submitForm">
        <div class="mb-3">
          <label for="service_name" class="form-label">Service Name</label>
          <input
            type="text"
            class="form-control"
            id="service_name"
            v-model="service.service_name"
            required
            placeholder="Enter service name"
          />
        </div>

        <div class="mb-3">
          <label for="base_price" class="form-label">Base Price</label>
          <input
            type="number"
            class="form-control"
            id="base_price"
            v-model="service.base_price"
            required
            placeholder="Enter base price"
            min="0"
            step="0.01"
          />
        </div>

        <div class="mb-3">
          <label for="description" class="form-label">Description</label>
          <textarea
            class="form-control"
            id="description"
            v-model="service.description"
            rows="4"
            placeholder="Enter a brief description of the service"
          ></textarea>
        </div>

        <div class="mb-3">
          <label for="time_required" class="form-label">Time Required (in minutes)</label>
          <input
            type="number"
            class="form-control"
            id="time_required"
            v-model="service.time_required"
            required
            placeholder="Enter time required for the service"
            min="1"
          />
        </div>

        <!-- Submit Button -->
        <div class="text-end">
          <button type="submit" class="btn btn-primary btn-lg" style="width: 200px;">
            Save Changes
          </button>
        </div>
      </form>
    </div>

    <!-- App Footer -->
    <AppFooter />
  </div>
</template>

<script>
import AdminNavbar from "@/components/AdminNavbar.vue";
import AppFooter from "@/components/AppFooter.vue";
import instance from '@/axios.js'; // Importing axios instance

export default {
  components: {
    AdminNavbar,
    AppFooter,
  },
  data() {
    return {
      service: {
        service_id: null,  // Initially null, will be set dynamically
        service_name: "",
        base_price: 0,
        description: "",
        time_required: 0,
      },
    };
  },
  mounted() {
    this.fetchServiceDetails();  // Fetch service details when component is mounted
  },

  methods: {
    // Fetch service details using service ID passed in the URL
    async fetchServiceDetails() {
      const serviceId = this.$route.params.id; // Get the service ID from the URL
      if (!serviceId) {
        alert("Service ID is missing");
        return;
      }
      
      try {
        // Make a GET request to fetch the service details
        const response = await instance.get(`/get_service_basedon_id/${serviceId}`);
        this.service = response.data;  // Set the service data from API response
      } catch (error) {
        console.error("Failed to fetch service details:", error.response?.data || error.message);
        alert("Failed to load service details. Please try again.");
      }
    },

    // Submit the form with updated service data
    async submitForm() {
      const serviceId = this.service.service_id;
      if (!serviceId) {
        alert("Service ID is missing. Cannot update.");
        return;
      }

      try {
        // Send the updated service data using PUT request
        const response = await instance.put(`/update_service/${serviceId}`, this.service);
        console.log("Service updated:", response.data);
        alert("Service updated successfully!");

        // Redirect to admin dashboard after successful update
        this.$router.push('/admin_dashboard');
      } catch (error) {
        console.error("Failed to update service:", error.response?.data || error.message);
        alert("Failed to update service. Please try again.");
      }
    },
  },
};
</script>

<style scoped>
.container-fluid {
  padding: 2rem;
}

.text-center {
  font-weight: bold;
}

.form-control {
  width: 100%;
}

.btn-primary {
  background-color: #004aad;
  border-color: #004aad;
}

.btn-primary:hover {
  background-color: #003388;
  border-color: #003388;
}
</style>
