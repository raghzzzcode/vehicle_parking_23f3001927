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
import instance from '@/axios.js';

export default {
  name: 'AdminAddService',
  components: {
    AdminNavbar,
    AppFooter
  },
  data() {
    return {
      service: {
        service_name: '',
        base_price: 0,
        description: '',
        time_required: 0
      }
    };
  },
  methods: {
    async submitForm() {
  try {
    const response = await instance.post('add_service', this.service);
    console.log('Service Added:', response.data);
    alert('Service added successfully!');
    
    // Redirect to admin dashboard after successful service addition
    this.$router.push({ name: 'admin_dashboard' });

    this.resetForm();
  } catch (error) {
    console.error('Error adding service:', error.response?.data || error.message);
    alert('Failed to add service. Please try again.');
  }
},
    resetForm() {
      this.service = {
        service_name: '',
        base_price: 0,
        description: '',
        time_required: 0
      };
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
