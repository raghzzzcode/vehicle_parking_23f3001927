<template>
    <nav class="navbar navbar-expand-lg shadow mb-4" style="background: linear-gradient(to bottom, #0066cc, #004aad);">
      <div class="container-fluid">
        <a class="navbar-brand ms-3" href="#" style="color: #ffffff;">Welcome to Professional</a>
        <div class="collapse navbar-collapse justify-content ms-5">
          <ul class="navbar-nav">
            <li class="nav-item">
              <a class="nav-link" href="/professional_dashboard" style="color: #ffffff;">Home</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/professional_search" style="color: #ffffff;">Search</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/professional_summary" style="color: #ffffff;">Summary</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/logout" style="color: #ffffff;">Logout</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </template>
  
  <script>
  export default {
    name: 'ProfessionalNavbar',
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
    color: #ffffff;
  }
  
  .nav-link:hover {
    color: #ffbb33;
  }
  </style>
  