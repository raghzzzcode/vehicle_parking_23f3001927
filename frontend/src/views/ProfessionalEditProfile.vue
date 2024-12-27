<template>
    <div>
      <ProfessionalNavbar />
      
      <div class="container mt-5 d-flex justify-content-center align-items-center" style="min-height: 100vh;">
        <div class="card shadow-lg rounded" style="background: linear-gradient(135deg, #004aad, #0099ff); width: 100%; max-width: 600px; padding: 20px;">
          <div class="card-body text-white d-flex flex-column align-items-center">
            <h4 class="card-title text-center mb-4">Edit Profile</h4>
  
            <!-- Flash message section -->
            <div v-if="flashMessage" :class="['alert', `alert-${flashMessage.type}`, 'alert-dismissible', 'fade', 'show']" role="alert">
              {{ flashMessage.message }}
              <button type="button" class="close" @click="flashMessage = null" aria-label="Close">
                <span aria-hidden="true">&times;</span>
              </button>
            </div>
  
            <!-- Edit Profile Form -->
            <form @submit.prevent="updateProfile" enctype="multipart/form-data">
              <!-- Email (readonly) -->
              <div class="mb-3">
                <label for="email" class="form-label">Email</label>
                <input type="email" class="form-control" id="email" v-model="formData.email" readonly>
              </div>
  
              <!-- Password -->
              <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input type="password" class="form-control" id="password" v-model="formData.password" placeholder="Leave blank to keep current password">
              </div>
  
              <!-- Full Name -->
              <div class="mb-3">
                <label for="fullname" class="form-label">Full Name</label>
                <input type="text" class="form-control" id="fullname" v-model="formData.fullname" required>
              </div>
  
              <!-- Service Name -->
              <div class="mb-3">
                <label for="service_name" class="form-label">Service Name</label>
                <input type="text" class="form-control" id="service_name" v-model="formData.serviceName" required>
              </div>
  
              <!-- Experience -->
              <div class="mb-3">
                <label for="experience" class="form-label">Experience (years)</label>
                <input type="number" class="form-control" id="experience" v-model="formData.experience" required>
              </div>
  
              <!-- Document -->
              <div class="mb-3">
                <label for="document" class="form-label">Upload Document</label>
                <input type="file" class="form-control" id="document" @change="handleFileChange" ref="fileInput">
              </div>
  
              <!-- Address -->
              <div class="mb-3">
                <label for="address" class="form-label">Address</label>
                <input type="text" class="form-control" id="address" v-model="formData.address" required>
              </div>
  
              <!-- Pincode -->
              <div class="mb-3">
                <label for="pincode" class="form-label">Pincode</label>
                <input type="text" class="form-control" id="pincode" v-model="formData.pincode" required>
              </div>
  
              <!-- Role (disabled) -->
              <div class="mb-3">
                <label for="role" class="form-label">Role</label>
                <input type="text" class="form-control" id="role" v-model="formData.role" readonly disabled>
              </div>
  
              <!-- Status (disabled) -->
              <div class="mb-3">
                <label for="status" class="form-label">Status</label>
                <input type="text" class="form-control" id="status" v-model="formData.status" readonly disabled>
              </div>
  
              <!-- Submit Button -->
              <button type="submit" class="btn btn-light w-100 mt-4" style="color: #004aad; font-weight: bold;">
                Save Changes
              </button>
            </form>
          </div>
        </div>
      </div>
  
      <AppFooter />
    </div>
  </template>
  
  <script>
    import ProfessionalNavbar from '@/components/ProfessionalNavbar.vue'
    import AppFooter from '@/components/AppFooter.vue'
  export default {
    name: 'ProfessionalEditProfile',
    components: {
      ProfessionalNavbar,
      AppFooter
    },
    data() {
      return {
        flashMessage: null,
        formData: {
          email: 'professional@example.com',
          password: '',
          fullname: 'John Doe',
          serviceName: 'Professional Service',
          experience: 5,
          address: '123 Main St',
          pincode: '123456',
          role: 'Professional',
          status: 'Active'
        },
        document: null
      }
    },
    methods: {
  handleFileChange(event) {
    this.document = event.target.files[0];
  },
  async updateProfile() {
    // Prepare form data to send to the backend
    const formData = new FormData();
    formData.append('full_name', this.formData.fullname);
    formData.append('service_name', this.formData.serviceName);
    formData.append('experience', this.formData.experience);
    formData.append('address', this.formData.address);
    formData.append('pincode', this.formData.pincode);
    if (this.document) {
      formData.append('document', this.document);
    }

    // Send a PUT request to update the professional profile
    try {
      const response = await fetch(`/api/professional/${this.formData.professional_id}`, {
        method: 'PUT',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to update profile');
      }

      const data = await response.json();
      this.flashMessage = {
        type: 'success',
        message: data.message,
      };
    } catch (error) {
      this.flashMessage = {
        type: 'danger',
        message: 'An error occurred while updating the profile.',
      };
    }
  }
}

  }
  </script>
  
  <style scoped>
  .card {
    border-radius: 10px;
  }
  </style>
  