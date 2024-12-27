<template>
  <div>
    <!-- Navbar -->
    <AppNavbar />
  
    <!-- Main Content -->
    <div class="container my-5">
      <h1 class="text-center text-primary mb-4">Homies : A to Z Household Services</h1>
  
      <div class="card p-4 rounded shadow mx-auto" style="max-width: 500px; background: linear-gradient(135deg, #004aad, #0099ff);">
        <div class="mb-4 text-end">
          <h2 class="text-white fs-5">
            <router-link to="professional_register" class="text-light">Register as Professional</router-link>
          </h2>
        </div>
  
        <!-- Flash messages -->
        <div v-if="messages.length > 0">
          <div v-for="(message, index) in messages" :key="index" :class="`alert alert-${message.category} alert-dismissible fade show`" role="alert">
            {{ message.text }}
            <button type="button" class="close" @click="closeMessage(index)" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
        </div>
  
        <!-- Login Form -->
        <form @submit.prevent="handleLogin">
          <div class="mb-3 row">
            <label for="email" class="col-md-4 col-form-label text-white">Registered Email ID:</label>
            <div class="col-md-8">
              <input type="email" v-model="email" class="form-control" id="email" placeholder="Enter your email" required style="background-color: #e0f7fa;">
            </div>
          </div>
          <div class="mb-3 row">
            <label for="password" class="col-md-4 col-form-label text-white">Password:</label>
            <div class="col-md-8">
              <input type="password" v-model="password" class="form-control" id="password" placeholder="Enter your password" required style="background-color: #e0f7fa;">
            </div>
          </div>
          <button type="submit" class="btn btn-light btn-lg w-100">Login</button>
        </form>
  
        <div class="text-center mt-3">
          <p class="text-white">Don't have an account? <router-link to="/customer_register" class="text-light">Create Account</router-link></p>
        </div>
      </div>
    </div>
  
    <!-- Footer -->
    <AppFooter />
  </div>
</template>

<script>
import AppNavbar from '@/components/AppNavbar.vue';
import AppFooter from '@/components/AppFooter.vue';
import instance from '@/axios.js';

export default {
  name: 'AllLogin',
  components: {
    AppNavbar,
    AppFooter,
  },
  data() {
    return {
      email: '',
      password: '',
      messages: []
    };
  },
  methods: {
    async handleLogin() {
  try {
    const response = await instance.post('login', {
      email: this.email,
      password: this.password
    });

    if (response.data.success) {
      this.messages.push({ category: 'success', text: 'Login successful!' });
      
      // Check the role and redirect accordingly
      const role = response.data.role;
      if (role === 'admin') {
        this.$router.push('/admin_dashboard');
      } else if (role === 'customer') {
        this.$router.push('/customer_dashboard');
      } else if (role === 'professional') {
        this.$router.push('/professional_dashboard');
      }
    } else {
      this.messages.push({ category: 'danger', text: 'Invalid credentials. Please try again.' });
    }
  } catch (error) {
    console.error(error);
    this.messages.push({ category: 'danger', text: 'An error occurred while logging in. Please try again.' });
  }
}

  }
};
</script>

<style scoped>
/* Your custom styles here */
</style>
