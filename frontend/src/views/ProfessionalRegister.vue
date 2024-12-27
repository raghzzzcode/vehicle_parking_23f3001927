<template>
  <div>
    <!-- Navbar Component -->
    <AppNavbar />
  
    <!-- Main content -->
    <div class="content-wrapper d-flex justify-content-center align-items-center">
      <div class="p-4 shadow-lg rounded" style="max-width: 450px; width: 100%; background: linear-gradient(to bottom, #0066cc, #004aad); color: #ffffff;">
        <h2 class="text-center mb-4" style="color: #ffffff;">Service Professional Sign Up</h2>
  
        <!-- Flash messages -->
        <div v-if="messages.length > 0">
          <div v-for="(message, index) in messages" :key="index" :class="`alert alert-${message.category} alert-dismissible fade show`" role="alert">
            {{ message.text }}
            <button type="button" class="close" @click="closeMessage(index)" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
        </div>
  
        <!-- Form to register a new professional -->
        <form @submit.prevent="handleRegister">
          <div class="mb-3">
            <label for="email" class="form-label">Email ID (Username)</label>
            <input type="email" v-model="form.email" class="form-control" id="email" required style="border: none; background-color: #e0f0ff;">
          </div>
          <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <input type="password" v-model="form.password" class="form-control" id="password" required style="border: none; background-color: #e0f0ff;">
          </div>
          <div class="mb-3">
            <label for="fullname" class="form-label">Fullname</label>
            <input type="text" v-model="form.fullname" class="form-control" id="fullname" required style="border: none; background-color: #e0f0ff;">
          </div>
          
          <!-- Service Dropdown -->
          <div class="mb-3">
            <label for="service_id" class="form-label">Service</label>
            <select v-model="form.service_id" class="form-control" id="service_id" required style="border: none; background-color: #e0f0ff;">
              <option value="" disabled>Select a service</option>
              <option v-for="service in services" :key="service.service_id" :value="service.service_id">
                {{ service.service_name }}
              </option>
            </select>
          </div>

          <div class="mb-3">
            <label for="experience" class="form-label">Experience (in years)</label>
            <input type="text" v-model="form.experience" class="form-control" id="experience" required style="border: none; background-color: #e0f0ff;">
          </div>
          <div class="mb-3">
            <label for="documents" class="form-label">Attach Documents (single PDF)</label>
            <input type="file" @change="handleFileUpload" class="form-control" id="documents" accept=".pdf" required style="border: none; background-color: #e0f0ff;">
          </div>
          <div class="mb-3">
            <label for="address" class="form-label">Address</label>
            <input type="text" v-model="form.address" class="form-control" id="address" required style="border: none; background-color: #e0f0ff;">
          </div>
          <div class="mb-3">
            <label for="pincode" class="form-label">Pincode</label>
            <input type="text" v-model="form.pincode" class="form-control" id="pincode" required style="border: none; background-color: #e0f0ff;">
          </div>
          <button type="submit" class="btn btn-light w-100 mt-4" style="color: #004aad; font-weight: bold;">
            Register
          </button>
        </form>
  
        <p class="text-center mt-3">
          <router-link to="/alllogin" class="text-white" style="text-decoration: underline;">Already have an account? Login here</router-link>
        </p>
      </div>
    </div>
  
    <!-- Footer Component -->
    <AppFooter />
  </div>
</template>

<script>
import AppNavbar from "@/components/AppNavbar.vue";
import AppFooter from "@/components/AppFooter.vue";
import instance from '@/axios.js';

export default {
  name: "ProfessionalRegister",
  components: {
    AppNavbar,
    AppFooter,
  },
  data() {
    return {
      form: {
        email: "",
        password: "",
        fullname: "",
        service_id: null,  // Changed to store service_id
        experience: "",  // Experience remains a string
        documents: null,
        address: "",
        pincode: "",
      },
      services: [],  // To store fetched services
      messages: [], // Flash messages
    };
  },
  created() {
    // Fetch available services when the component is created
    this.fetchServices();
  },
  methods: {
    fetchServices() {
      instance
        .get('get_services_for_prof_regis')  // Adjust to your API endpoint for fetching services
        .then((response) => {
          this.services = response.data.services;  // Assuming API returns list of services
        })
        .catch((error) => {
          console.error("Error fetching services:", error);
        });
    },
    handleRegister() {
      if (
        this.form.email &&
        this.form.password &&
        this.form.fullname &&
        this.form.service_id &&
        this.form.experience &&
        this.form.documents &&
        this.form.address &&
        this.form.pincode
      ) {
        // Send form data as-is, no conversion to number needed
        let formData = new FormData();
        formData.append('email', this.form.email);
        formData.append('password', this.form.password);
        formData.append('fullname', this.form.fullname);
        formData.append('service_id', this.form.service_id);
        formData.append('experience', this.form.experience);  // Keep experience as string
        formData.append('address', this.form.address);
        formData.append('pincode', this.form.pincode);
        formData.append('document', this.form.documents);

        // Send POST request to Flask backend
        instance
          .post('professional_register', formData)
          .then((response) => {
            this.messages.push({
              category: 'success',
              text: response.data.message,
            });
          })
          .catch((error) => {
            this.messages.push({
              category: 'danger',
              text: error.response.data.error,
            });
          });
      } else {
        this.messages.push({
          category: 'danger',
          text: 'Please fill in all required fields.',
        });
      }
    },
    closeMessage(index) {
      // Remove the message at the specified index
      this.messages.splice(index, 1);
    },
    handleFileUpload(event) {
      // Handle file upload
      this.form.documents = event.target.files[0];
    },
  },
};
</script>

<style scoped>
.content-wrapper {
  min-height: calc(90vh - 60px); /* Adjust to leave space for the navbar */
  margin-top: 60px; /* Ensure no content is under the navbar */
}
</style>
