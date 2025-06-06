<template>
  <div>
    <!-- Navbar Component -->
    <AppNavbar />

    <!-- Main content -->
    <div class="content-wrapper d-flex justify-content-center align-items-center">
      <div class="p-4 shadow-lg rounded" style="max-width: 400px; width: 100%; background: linear-gradient(to bottom, #0066cc, #004aad); color: #ffffff;">
        <h2 class="text-center mb-4" style="color: #ffffff;">Customer Sign Up</h2>

        <!-- Flash messages -->
        <div v-if="messages.length > 0">
          <div v-for="(message, index) in messages" :key="index" :class="`alert alert-${message.category} alert-dismissible fade show`" role="alert">
            {{ message.text }}
            <button type="button" class="close" @click="closeMessage(index)" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
        </div>

        <!-- Form to register a new user -->
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
  name: "CustomerRegister",
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
        address: "",
        pincode: "",
      },
      messages: [], // Flash messages
    };
  },
  methods: {
    closeMessage(index) {
      // Remove message from the messages array
      this.messages.splice(index, 1);
    },
    async handleRegister() {
      // Check if all required fields are filled
      if (this.form.email && this.form.password && this.form.fullname && this.form.address && this.form.pincode) {
        try {
          // Make the API call to register the customer
          const response = await instance.post('customer_register', this.form);
          this.messages.push({
            category: 'success',
            text: response.data.message
          });
        } catch (error) {
          // Handle error
          const errorMsg = error.response?.data?.error || 'Registration failed';
          this.messages.push({
            category: 'danger',
            text: errorMsg
          });
        }
      } else {
        this.messages.push({
          category: 'danger',
          text: 'Please fill in all required fields.'
        });
      }
    }
  },
};
</script>

<style scoped>
.content-wrapper {
  min-height: calc(90vh - 60px); /* Ensures space for the navbar */
  margin-top: 60px; /* Prevents content from being under the navbar */
}
</style>
