<template>
  <nav class="navbar navbar-expand-lg navbar-light">
    <div class="container-fluid">
      <!-- Homepage Link -->
      <a class="navbar-brand text-white" href="/">Household Services</a>
      
      <!-- Toggler Button for Small Screens -->
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      
      <!-- Navbar Links -->
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <a class="nav-link text-white" href="/">Home</a> <!-- New Home Link -->
          </li>
          <li class="nav-item">
            <a class="nav-link text-white" href="/alllogin">
              <i class="bi bi-box-arrow-in-right"></i> Login
            </a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'AppNavbar'
}
</script>

<style scoped>
/* Navbar specific styles */
body {
  background: linear-gradient(to bottom right, #e7f1ff, #b3d7ff);
  font-family: Arial, sans-serif;
  line-height: 1.6;
  color: #333; /* Set body text color for contrast */
}

nav {
  background-color: #0056b3;
  border-bottom: 2px solid #003d7a;
}

nav .navbar-brand,
nav .nav-link {
  color: #ffffff !important;
}

nav .nav-link:hover {
  text-decoration: underline;
  color: #d1e4ff !important;
}

.navbar-toggler-icon {
  background-color: white;
}
</style>

