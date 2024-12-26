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
  
  export default {
    components: {
      AdminNavbar,
      AppFooter,
    },
    data() {
      return {
        service: {
          id: 1,
          service_name: "Service Example",
          base_price: 100.0,
        },
      };
    },
    methods: {
      submitForm() {
        // Placeholder for form submission logic
        console.log("Service updated:", this.service);
        // Here, you can make an API call to update the service details
      },
    },
  };
  </script>
  
  <style scoped>
  /* You can add custom styles here if needed */
  </style>
  