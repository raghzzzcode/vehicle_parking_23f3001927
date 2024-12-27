<template>
  <div>
    <!-- Include Professional Navbar -->
    <ProfessionalNavbar />

    <div class="container mt-5 d-flex justify-content-center align-items-center" style="min-height: 80vh;">
      <div class="card shadow-lg rounded" style="background: linear-gradient(135deg, #004aad, #0099ff); width: 100%; max-width: 400px; padding: 20px;">
        <div class="card-body text-white d-flex flex-column align-items-center">
          <!-- Profile Name -->
          <h4 class="card-title text-center mb-4">{{ professional.fullName }}</h4>

          <!-- Profile Details -->
          <div class="profile-details w-100">
            <p><i class="fas fa-envelope"></i> <strong>Email:</strong> {{ professional.email }}</p>
            <p><i class="fas fa-cogs"></i> <strong>Service Name:</strong> {{ professional.serviceName }}</p>
            <p><i class="fas fa-briefcase"></i> <strong>Experience:</strong> {{ professional.experience }} years</p>
            <p><i class="fas fa-map-marker-alt"></i> <strong>Address:</strong> {{ professional.address }}</p>
            <p><i class="fas fa-thumbtack"></i> <strong>Pincode:</strong> {{ professional.pincode }}</p>
            <p><i class="fas fa-user-tie"></i> <strong>Role:</strong> {{ professional.role }}</p>

            <!-- Status Section -->
            <p v-if="professional.status">
              <i class="fas fa-check-circle"></i> <strong>Status:</strong> <span class="badge bg-info">{{ professional.status }}</span>
            </p>
            <p v-else>
              <i class="fas fa-times-circle"></i> <strong>Status:</strong> <span class="badge bg-secondary">N/A</span>
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Include Footer -->
    <AppFooter />
  </div>
</template>

<script>
import instance from '@/axios.js';
import ProfessionalNavbar from '@/components/ProfessionalNavbar.vue';
import AppFooter from '@/components/AppFooter.vue';

export default {
  components: {
    ProfessionalNavbar,
    AppFooter
  },
  data() {
    return {
      professional: {} // To store professional data
    };
  },
  mounted() {
    // Fetch professional data when the component is mounted
    const professionalId = this.$route.params.professionalId; // Get dynamic ID from the route params
    if (professionalId) {
      instance.get(`view_professional/${professionalId}`)
        .then(response => {
          this.professional = response.data;
        })
        .catch(error => {
          console.error('There was an error fetching the professional data:', error);
        });
    }
  }
};
</script>

<style scoped>
/* Custom styling for the profile page */
.card-title {
  font-size: 1.8rem;
  font-weight: bold;
}

.card-body {
  background-color: rgba(0, 0, 0, 0.3);
  border-radius: 10px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}

.profile-details p {
  font-size: 1.1rem;
  margin-bottom: 10px;
}

.profile-details i {
  margin-right: 10px;
}

.badge {
  font-size: 0.9rem;
}
</style>
