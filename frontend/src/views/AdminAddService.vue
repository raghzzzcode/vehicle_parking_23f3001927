<template>
    <div>
      <!-- Admin Navbar -->
      <AdminNavbar />
  
      <div class="container-fluid mb-5">
        <!-- Add New Service Section -->
        <h3 class="text-center mb-4" style="color: #004aad;">Add New Service</h3>
  
        <!-- Service Add Form -->
        <form @submit.prevent="submitForm">
          <div class="mb-3">
            <label for="service_id" class="form-label">Service ID</label>
            <input type="text" class="form-control" id="service_id" v-model="service.id" required placeholder="Enter service ID">
          </div>
  
          <div class="mb-3">
            <label for="service_name" class="form-label">Service Name</label>
            <input type="text" class="form-control" id="service_name" v-model="service.name" required placeholder="Enter service name">
          </div>
  
          <div class="mb-3">
            <label for="base_price" class="form-label">Base Price</label>
            <input type="number" class="form-control" id="base_price" v-model="service.basePrice" required placeholder="Enter base price" min="0" step="0.01">
          </div>
  
          <div class="text-end">
            <button type="submit" class="btn btn-primary btn-lg" style="width: 200px;">Save Service</button>
          </div>
        </form>
      </div>
  
      <!-- App Footer -->
      <AppFooter />
    </div>
  </template>
  
  <script>
  import AdminNavbar from '@/components/AdminNavbar.vue';
  import AppFooter from '@/components/AppFooter.vue';
  
  export default {
    name: 'AdminAddService',
    components: {
      AdminNavbar,
      AppFooter
    },
    data() {
      return {
        service: {
          id: '',
          name: '',
          basePrice: 0
        }
      };
    },
    methods: {
      submitForm() {
        // Handle form submission logic here
        console.log('Service Added:', this.service);
        // You can add the logic to send the form data to the backend
      }
    }
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
  