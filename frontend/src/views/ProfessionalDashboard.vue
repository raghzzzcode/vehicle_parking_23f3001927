<template>
  <div>
    <!-- Include Professional Navbar -->
    <ProfessionalNavbar />

    <!-- Profile Section -->
    <div class="container">
      <div class="row justify-content-end mb-4">
        <div class="col-auto">
          <div class="card shadow-sm border-0" style="width: 300px;">
            <div class="card-body">
              <h5 class="card-title" style="color: #004aad;">Profile</h5>
              <p class="card-text">View or edit your professional details below:</p>
              <div class="d-flex justify-content-between">
                <form @submit.prevent="viewProfile">
                  <button type="submit" class="btn btn-primary">View Profile</button>
                </form>
                <form @submit.prevent="editProfile">
                  <button class="btn btn-outline-primary">Edit Profile</button>
                </form>
              </div>  
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Today Services Section -->
    <div class="container-fluid">
      <div class="mb-5">
        <h3 class="text-center mb-3" style="color: #004aad;">Today Services</h3>
        <table class="table table-striped table-hover shadow rounded">
          <thead style="background-color: #004aad; color: white;">
            <tr>
              <th>ID</th>
              <th>Customer Name</th>
              <th>Email</th>
              <th>Location</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="service in todayServices" :key="service.id">
              <td>{{ service.id }}</td>
              <td>{{ service.customer_name }}</td>
              <td>{{ service.email }}</td>
              <td>{{ service.location }}</td>
              <td>
                <form @submit.prevent="acceptService(service.id)" style="display:inline;">
                  <button type="submit" class="btn btn-outline-primary btn-sm">Accept</button>
                </form>
                <form @submit.prevent="rejectService(service.id)" style="display:inline;">
                  <button type="submit" class="btn btn-outline-danger btn-sm">Reject</button>
                </form>
              </td>
            </tr>
            <tr v-if="!todayServices.length">
              <td colspan="5" class="text-center">No services available today.</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Closed Services Section -->
      <div class="mb-5">
        <h3 class="text-center mb-3" style="color: #004aad;">Closed Services</h3>
        <table class="table table-striped table-hover shadow rounded">
          <thead style="background-color: #004aad; color: white;">
            <tr>
              <th>ID</th>
              <th>Customer Name</th>
              <th>Email</th>
              <th>Location</th>
              <th>Date</th>
              <th>Rating</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="service in closedServices" :key="service.id">
              <td>{{ service.id }}</td>
              <td>{{ service.customer_name }}</td>
              <td>{{ service.email }}</td>
              <td>{{ service.location }}</td>
              <td>{{ service.date }}</td>
              <td>
                <span v-if="service.rating">{{ '⭐'.repeat(service.rating) }}</span>
                <span v-else>No rating</span>
              </td>
            </tr>
            <tr v-if="!closedServices.length">
              <td colspan="6" class="text-center">No closed services available.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Include App Footer -->
    <AppFooter />
  </div>
</template>

<script>
import instance from '@/axios.js';
import ProfessionalNavbar from '@/components/ProfessionalNavbar.vue';
import AppFooter from '@/components/AppFooter.vue';

export default {
  name: 'ProfessionalDashboard',
  components: {
    ProfessionalNavbar,
    AppFooter
  },
  data() {
    return {
      todayServices: [],
      closedServices: []
    };
  },
  created() {
    this.fetchProfile();
    this.fetchTodayServices();
    this.fetchClosedServices();
  },
  methods: {
    async fetchProfile() {
      try {
        const response = await instance.get('professional_profile', {
          params: { professional_id: 1 }  // Replace with actual professional ID
        });
        console.log('Profile:', response.data);
      } catch (error) {
        console.error('Error fetching profile:', error);
      }
    },
    async fetchTodayServices() {
      try {
        const response = await instance.get('professional/today-services');
        this.todayServices = response.data;
      } catch (error) {
        console.error('Error fetching today\'s services:', error);
      }
    },
    async fetchClosedServices() {
      try {
        const response = await instance.get('professional/closed-services');
        this.closedServices = response.data;
      } catch (error) {
        console.error('Error fetching closed services:', error);
      }
    },
    async acceptService(serviceId) {
      try {
        const response = await instance.post('professional/accept-service', {
          request_id: serviceId,
          professional_id: 1  // Replace with actual professional ID
        });
        console.log('Service accepted:', response.data);
        this.fetchTodayServices();  // Refresh the services list
      } catch (error) {
        console.error('Error accepting service:', error);
      }
    },
    async rejectService(serviceId) {
      try {
        const response = await instance.post('professional/reject-service', {
          request_id: serviceId
        });
        console.log('Service rejected:', response.data);
        this.fetchTodayServices();  // Refresh the services list
      } catch (error) {
        console.error('Error rejecting service:', error);
      }
    }
  }
};
</script>

<style scoped>
/* Button and Table Styling */
.btn-primary, .btn-outline-primary, .btn-outline-danger {
  font-weight: bold;
  transition: background-color 0.3s, transform 0.3s, box-shadow 0.3s;
}

.btn-outline-primary {
  border-color: #004aad;
  color: #004aad;
}

.btn-outline-primary:hover {
  background-color: #004aad;
  color: white;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}

.btn-outline-danger {
  border-color: #dc3545;
  color: #dc3545;
}

.btn-outline-danger:hover {
  background-color: #dc3545;
  color: white;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}

/* Table Styling */
table {
  border-radius: 8px;
  overflow: hidden;
}

thead {
  background-color: #004aad;
  color: white;
}

thead th {
  font-weight: 600;
  font-size: 16px;
}

tbody tr {
  background-color: #f9f9f9;
  transition: background-color 0.3s;
}

tbody tr:hover {
  background-color: #e1f5fe;
}

tbody td {
  font-size: 14px;
}

.table-striped tbody tr:nth-of-type(odd) {
  background-color: #f1f1f1;
}
</style>
