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
              <a :href="'/admin_edit_service/' + service.id" class="btn btn-outline-primary btn-sm">Edit</a>
              <form @submit.prevent="deleteService(service.id)" style="display:inline;">
                <button type="submit" class="btn btn-outline-danger btn-sm">Delete</button>
              </form>
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Add New Service Button -->
      <div class="text-end mb-5">
        <a href="/admin_add_service" class="btn btn-primary btn-lg" style="width: 200px; background-color: #0066cc; border-color: #005bb5;">+ New Service</a>
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
      services: [],
      professionals: [],
      serviceRequests: []
    };
  },
  methods: {
    async fetchServices() {
      try {
        const response = await fetch('/api/services');
        if (response.ok) {
          this.services = await response.json();
        }
      } catch (error) {
        console.log('Error fetching services:', error);
      }
    },

    async fetchProfessionals() {
      try {
        const response = await fetch('/api/professionals');
        if (response.ok) {
          this.professionals = await response.json();
        }
      } catch (error) {
        console.log('Error fetching professionals:', error);
      }
    },

    async fetchServiceRequests() {
      try {
        const response = await fetch('/api/service_requests');
        if (response.ok) {
          this.serviceRequests = await response.json();
        }
      } catch (error) {
        console.log('Error fetching service requests:', error);
      }
    },

    async deleteService(id) {
      try {
        const response = await fetch(`/api/services/${id}`, {
          method: 'DELETE',
        });
        if (response.ok) {
          this.services = this.services.filter(service => service.id !== id);
          console.log(`Service with ID ${id} deleted`);
        } else {
          console.log('Failed to delete service');
        }
      } catch (error) {
        console.log('Error deleting service:', error);
      }
    },

    async approveProfessional(id) {
      try {
        const response = await fetch(`/api/professionals/${id}/approve`, {
          method: 'POST',
        });
        if (response.ok) {
          const professional = this.professionals.find(p => p.id === id);
          professional.status = 'approved';
          console.log(`Professional with ID ${id} approved`);
        } else {
          console.log('Failed to approve professional');
        }
      } catch (error) {
        console.log('Error approving professional:', error);
      }
    },

    async rejectProfessional(id) {
      try {
        const response = await fetch(`/api/professionals/${id}/reject`, {
          method: 'POST',
        });
        if (response.ok) {
          const professional = this.professionals.find(p => p.id === id);
          professional.status = 'rejected';
          console.log(`Professional with ID ${id} rejected`);
        } else {
          console.log('Failed to reject professional');
        }
      } catch (error) {
        console.log('Error rejecting professional:', error);
      }
    },

    async deleteProfessional(id) {
      try {
        const response = await fetch(`/api/professionals/${id}`, {
          method: 'DELETE',
        });
        if (response.ok) {
          this.professionals = this.professionals.filter(prof => prof.id !== id);
          console.log(`Professional with ID ${id} deleted`);
        } else {
          console.log('Failed to delete professional');
        }
      } catch (error) {
        console.log('Error deleting professional:', error);
      }
    }
  },
  created() {
    this.fetchServices();
    this.fetchProfessionals();
    this.fetchServiceRequests();
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
