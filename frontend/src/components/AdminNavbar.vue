<template>
    <nav class="navbar navbar-expand-lg shadow mb-4" style="background: linear-gradient(to bottom, #0066cc, #004aad);">
      <div class="container-fluid">
        <a class="navbar-brand ms-3" href="#" style="color: #ffffff;">Welcome to Admin Dashboard</a>
        <div class="collapse navbar-collapse justify-content ms-5">
          <ul class="navbar-nav">
            <li class="nav-item">
              <router-link class="nav-link" to="/admin_dashboard" style="color: #ffffff;">Home</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/admin_search" style="color: #ffffff;">Search</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/admin_summary" style="color: #ffffff;">Summary</router-link>
            </li>
            <li class="nav-item">
              <router-link class="nav-link" to="/logout" style="color: #ffffff;">Logout</router-link>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </template>
  
  <script>
  export default {
    name: 'AdminNavbar'
  };
  </script>
  
  <style scoped>
  .navbar {
    background: linear-gradient(to bottom, #0066cc, #004aad);
  }
  
  .navbar-brand {
    color: #ffffff;
  }
  
  .nav-link {
    color: #ffffff !important;
  }
  
  .nav-link:hover {
    color: #d6d6d6 !important;
  }
  </style>
  