<template>
    <div>
      <!-- Admin Navbar -->
      <AdminNavbar />
  
      <div class="container-fluid mb-5">
  
        <!-- Services Section -->
        <h3 class="text-center mb-4" style="color: #003366;">Services</h3>
        <table class="table table-striped table-hover shadow rounded">
          <thead style="background-color: #cce5ff; color: #003366;">
            <tr>
              <th>ID</th>
              <th>Service Name</th>
              <th>Base Price</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(service, index) in services" :key="service.id" :style="{ backgroundColor: index % 2 === 0 ? '#f4faff' : '#ffffff' }">
              <td><a href="#" style="color: #004aad;">{{ service.id }}</a></td>
              <td>{{ service.name }}</td>
              <td>${{ service.basePrice }}</td>
              <td>
                <a :href="'/user/admin_editservice/' + service.id" class="btn btn-outline-primary btn-sm">Edit</a>
                <form @submit.prevent="deleteService(service.id)" style="display:inline;">
                  <button type="submit" class="btn btn-outline-danger btn-sm">Delete</button>
                </form>
              </td>
            </tr>
          </tbody>
        </table>
  
        <!-- Add New Service Button -->
        <div class="text-end mb-5">
          <a href="/user/admin_addservice" class="btn btn-primary btn-lg" style="width: 200px; background-color: #0066cc; border-color: #005bb5;">+ New Service</a>
        </div>
  
        <!-- Professionals Section -->
        <h3 class="text-center mb-4" style="color: #003366;">Professionals</h3>
        <table class="table table-striped table-hover shadow rounded">
          <thead style="background-color: #b3d9ff; color: #003366;">
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Experience (Yrs)</th>
              <th>Service Name</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(professional, index) in professionals" :key="professional.id" :style="{ backgroundColor: index % 2 === 0 ? '#f4faff' : '#ffffff' }">
              <td><a href="#" style="color: #004aad;">{{ professional.id }}</a></td>
              <td>{{ professional.name }}</td>
              <td>{{ professional.experience }}</td>
              <td>{{ professional.serviceName }}</td>
              <td>
                <span v-if="professional.status" class="badge bg-secondary">{{ professional.status }}</span>
                <template v-else>
                  <form @submit.prevent="approveProfessional(professional.id)" style="display:inline;">
                    <button type="submit" class="btn btn-outline-success btn-sm">Approve</button>
                  </form>
                  <form @submit.prevent="rejectProfessional(professional.id)" style="display:inline;">
                    <button type="submit" class="btn btn-outline-danger btn-sm">Reject</button>
                  </form>
                  <form @submit.prevent="deleteProfessional(professional.id)" style="display:inline;">
                    <button type="submit" class="btn btn-outline-warning btn-sm">Delete</button>
                  </form>
                </template>
              </td>
            </tr>
          </tbody>
        </table>
  
        <!-- Service Requests Section -->
        <h3 class="text-center mb-4" style="color: #003366;">Service Requests</h3>
        <table class="table table-striped table-hover shadow rounded">
          <thead style="background-color: #cce5ff; color: #003366;">
            <tr>
              <th>Service ID</th>
              <th>Assigned Professional (if any)</th>
              <th>Service Name</th>
              <th>Status (R/C)</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(request, index) in serviceRequests" :key="request.id" :style="{ backgroundColor: index % 2 === 0 ? '#f4faff' : '#ffffff' }">
              <td><a href="#" style="color: #004aad;">{{ request.id }}</a></td>
              <td>{{ request.professional || 'N/A' }}</td>
              <td>{{ request.serviceName }}</td>
              <td>{{ request.status || 'N/A' }}</td>
            </tr>
          </tbody>
        </table>
  
      </div>
  
      <!-- App Footer -->
      <AppFooter />
    </div>
  </template>
  
  <script>
  import AdminNavbar from '@/components/AdminNavbar.vue';
  import AppFooter from '@/components/AppFooter.vue';
  
  export default {
    name: 'AdminDashboard',
    components: {
      AdminNavbar,
      AppFooter
    },
    data() {
      return {
        services: [
          { id: 1, name: 'Web Development', basePrice: 300 },
          { id: 2, name: 'SEO Optimization', basePrice: 150 },
          { id: 3, name: 'App Development', basePrice: 500 }
        ],
        professionals: [
          { id: 1, name: 'John Doe', experience: 5, serviceName: 'Web Development', status: 'Approved' },
          { id: 2, name: 'Jane Smith', experience: 3, serviceName: 'SEO Optimization', status: '' },
          { id: 3, name: 'Michael Brown', experience: 4, serviceName: 'App Development', status: '' }
        ],
        serviceRequests: [
          { id: 1, professional: 'John Doe', serviceName: 'Web Development', status: 'Completed' },
          { id: 2, professional: '', serviceName: 'SEO Optimization', status: 'Pending' }
        ]
      };
    },
    methods: {
      deleteService(id) {
        this.services = this.services.filter(service => service.id !== id);
        console.log(`Service with ID ${id} deleted`);
      },
      approveProfessional(id) {
        const professional = this.professionals.find(prof => prof.id === id);
        if (professional) professional.status = 'Approved';
        console.log(`Professional with ID ${id} approved`);
      },
      rejectProfessional(id) {
        const professional = this.professionals.find(prof => prof.id === id);
        if (professional) professional.status = 'Rejected';
        console.log(`Professional with ID ${id} rejected`);
      },
      deleteProfessional(id) {
        this.professionals = this.professionals.filter(prof => prof.id !== id);
        console.log(`Professional with ID ${id} deleted`);
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
  
  .table th, .table td {
    vertical-align: middle;
  }
  
  .table-striped tbody tr:nth-child(odd) {
    background-color: #f4faff;
  }
  
  .table-hover tbody tr:hover {
    background-color: #e6f0ff;
  }
  
  .btn-outline-success:hover {
    background-color: #28a745;
    color: white;
  }
  
  .btn-outline-danger:hover {
    background-color: #dc3545;
    color: white;
  }
  
  .btn-outline-warning:hover {
    background-color: #ffc107;
    color: white;
  }
  </style>
  