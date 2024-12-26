<template>
    <div>
      <!-- Include Navbar -->
      <AppNavbar />
  
      <!-- Main content area -->
      <div class="container my-5" style="background-color: #d0e6ff; border-radius: 12px; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15); padding: 40px; transition: transform 0.2s;">
        <h1 class="text-center" style="color: #003d7a; font-weight: bold; margin-bottom: 30px;">Welcome to Homies</h1>
        <p class="text-center" style="color: #4a4a4a; font-size: 1.1rem;">Connecting you with trusted professionals for comprehensive home services</p>
  
        <div class="row text-center mt-5">
          <div class="col-md-4 mb-4">
            <div class="card shadow border-0" style="background-color: #e7f1ff; border-radius: 15px; overflow: hidden;">
              <img src="@/assets/customer.jpeg" alt="Customer" class="img-fluid uniform-image">
              <div class="card-body">
                <router-link to="/alllogin" class="btn btn-lg btn-primary" style="border-radius: 25px; font-size: 1.1rem;">
                  <i class="fas fa-user"></i> Customer Login
                </router-link>
                <p class="text-muted mt-3">Book services and manage requests</p>
              </div>
            </div>
          </div>
  
          <div class="col-md-4 mb-4">
            <div class="card shadow border-0" style="background-color: #e7f1ff; border-radius: 15px; overflow: hidden;">
              <img src="@/assets/service_prof.png" alt="Service Professional" class="img-fluid uniform-image">
              <div class="card-body">
                <router-link to="/alllogin" class="btn btn-lg btn-primary" style="border-radius: 25px; font-size: 1.1rem;">
                  <i class="fas fa-briefcase"></i> Service Professional Login
                </router-link>
                <p class="text-muted mt-3">View and accept service requests</p>
              </div>
            </div>
          </div>
  
          <div class="col-md-4 mb-4">
            <div class="card shadow border-0" style="background-color: #e7f1ff; border-radius: 15px; overflow: hidden;">
              <img src="@/assets/admin.png" alt="Admin" class="img-fluid uniform-image">
              <div class="card-body">
                <router-link to="/alllogin" class="btn btn-lg btn-primary" style="border-radius: 25px; font-size: 1.1rem;">
                  <i class="fas fa-cog"></i> Admin Login
                </router-link>
                <p class="text-muted mt-3">Monitor and manage the platform</p>
              </div>
            </div>
          </div>
        </div>
      </div>
  
      <!-- Include Footer -->
      <AppFooter />
    </div>
  </template>
  
  <script>
  import AppNavbar from '@/components/AppNavbar.vue';
  import AppFooter from '@/components/AppFooter.vue';

  export default {
    name: 'BaseLayout',
    components: {
      AppNavbar,
      AppFooter
    }
  }
  </script>
  
  <style scoped>
  /* You can add custom styles for your layout */
  body {
    background: linear-gradient(to bottom right, #dbe9ff, #aacdff);
    font-family: 'Helvetica Neue', sans-serif;
    line-height: 1.6;
  }
  
  .main-content {
    padding: 20px;
  }
  
  .home-page {
    text-align: center;
    padding: 40px 0;
  }
  
  .uniform-image {
    height: 220px;
    object-fit: cover;
    width: 100%;
    border-bottom-left-radius: 15px;
    border-bottom-right-radius: 15px;
  }
  
  .card {
    transition: transform 0.3s, box-shadow 0.3s;
  }
  
  .card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
  }
  
  h1, h2, h3, h4, h5, h6 {
    color: #003d7a;
  }
  
  p {
    color: #555;
  }
  
  .btn-primary {
    background-color: #0069d9;
    border: none;
  }
  
  .btn-primary:hover {
    background-color: #004a99;
  }
  </style>
  