<template>
    <nav class="navbar navbar-expand-lg shadow mb-4" style="background: linear-gradient(to bottom, #0066cc, #004aad);">
      <div class="container-fluid">
        <a class="navbar-brand ms-3" href="#" style="color: #ffffff;">Welcome to Customer</a>
        <div class="collapse navbar-collapse justify-content ms-5">
          <ul class="navbar-nav">
            <li class="nav-item">
              <router-link class="nav-link" to="/customer_dashboard" style="color: #ffffff;">Home</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/customer_search" style="color: #ffffff;">Search</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/customer_summary" style="color: #ffffff;">Summary</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/logout" style="color: #ffffff;">Logout</router-link>
            </li>
          </ul>
          <router-link to="/customer_profile" class="btn btn-light ms-auto" style="color: #004aad;">Profile</router-link>
        </div>
      </div>
    </nav>
  </template>
  
  <script>
  export default {
    name: 'CustomerNavbar',
  };
  </script>
  
  <style scoped>
  .navbar-nav .nav-link {
    font-size: 16px;
    font-weight: bold;
  }
  
  .navbar-nav .nav-link:hover {
    color: #c1c1c1;
  }
  
  .btn-light {
    color: #004aad;
    border: 1px solid #004aad;
    border-radius: 5px;
  }
  
  .btn-light:hover {
    background-color: #004aad;
    color: white;
  }
  </style>
  