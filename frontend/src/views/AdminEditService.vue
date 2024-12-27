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
import axios from "axios";

export default {
  components: {
    AdminNavbar,
    AppFooter,
  },
  data() {
    return {
      service: {
        service_id: 1, // Example ID, should be dynamically fetched
        service_name: "",
        base_price: 0,
        description: "",
        time_required: 0,
      },
    };
  },
  mounted() {
    this.fetchServiceDetails();
  },
  methods: {
    async fetchServiceDetails() {
      try {
        // Fetch the service details based on service_id (Example URL)
        const response = await axios.get(`/api/services/${this.service.service_id}`);
        this.service = response.data;
      } catch (error) {
        console.error("Failed to fetch service details:", error.response?.data || error.message);
      }
    },
    async submitForm() {
      try {
        // Update service details (Example URL)
        const response = await axios.put(`/api/services/${this.service.service_id}`, this.service);
        console.log("Service updated:", response.data);
        alert("Service updated successfully!");
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
