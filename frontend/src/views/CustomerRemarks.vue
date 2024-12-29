<template>
  <div>
    <!-- Customer Navbar -->
    <CustomerNavbar />
  
    <!-- Service Remarks Form Section -->
    <div class="container-fluid mb-5" style="max-width: 600px; margin-top: 30px;">
      <form @submit.prevent="submitRemarks" class="shadow p-4 rounded" style="border: 2px solid #ccc; background-color: #f9f9f9;">
        <h4 class="text-center text-primary mb-3">Service Remarks</h4>
        <p class="text-center text-primary">Request ID: {{ service.request_id }}</p>
  
        <!-- Service Details -->
        <div class="row mb-3">
          <input type="text" class="form-control text-center" :placeholder="service.service_name" disabled style="background-color: #f8d7da;">
        </div>
  
        <div class="row mb-3">
          <input type="text" class="form-control text-center" :placeholder="service.professional_name" disabled style="background-color: #f8d7da;">
        </div>
  
        <!-- Service Rating -->
        <div class="mb-3">
          <label class="form-label">Service rating:</label>
          <div class="rating">
            <span 
              v-for="(diamond, index) in diamonds" 
              :key="index" 
              :class="['diamond', {inactive: index >= rating}]" 
              @click="setRating(index)"
            >
              &#9670;
            </span>
          </div>
          <input type="hidden" v-model="rating" />
        </div>
  
        <!-- Remarks -->
        <div class="mb-4">
          <label class="form-label">Remarks (if any):</label>
          <textarea v-model="remarks" class="form-control" rows="3" placeholder="Enter your remarks here..." style="resize: none;"></textarea>
        </div>
  
        <!-- Buttons -->
        <div class="d-flex justify-content-between">
          <button type="submit" class="btn btn-primary btn-sm">Submit</button>
        </div>
      </form>
    </div>
  
    <!-- App Footer -->
    <AppFooter />
  </div>
</template>

<script>
import CustomerNavbar from "@/components/CustomerNavbar.vue";
import AppFooter from "@/components/AppFooter.vue";
import instance from '@/axios.js';  // Import the Axios instance

export default {
  name: "CustomerRemarks",
  components: {
    CustomerNavbar,
    AppFooter
  },
  data() {
    return {
      service: {
        service_name: this.$route.query.service_name,
        professional_name: this.$route.query.professional_name,
        request_id: this.$route.query.request_id
      },
      diamonds: [0, 1, 2, 3, 4], // Representing 5 rating diamonds
      rating: 3, // Default rating
      remarks: "", // Remarks entered by the user
      customer_email: this.$route.query.customer_email, // Fetch customer email from query params
      professional_email: this.$route.query.professional_email, // Fetch professional email from query params
      request_id: this.$route.query.request_id, // Fetch request_id from query params
      professional_name: "", // To store professional name
      service_name: "" // To store service name
    };
  },
  mounted() {
    this.fetchServiceDetails();
  },
  methods: {
    async fetchServiceDetails() {
      try {
        const response = await instance.get('insert_review', {
          params: {
            professional_email: this.professional_email,
            customer_email: this.customer_email,
            request_id: this.request_id
          }
        });

        if (response.data) {
          // Update service object with the response data
          this.service.service_name = response.data.service_name;
          this.service.professional_name = response.data.professional_name;
          this.service.request_id = response.data.request_id; // Assuming request_id is in response
        } else {
          alert('Service not found or already completed');
        }
      } catch (error) {
        console.error('Error fetching service details:', error);
      }
    },
    setRating(index) {
      this.rating = index + 1; // Set the rating value based on the diamond clicked
    },
    async submitRemarks() {
      const requestData = {
        request_id: this.service.request_id, // Use the service object request_id
        rating: this.rating,
        comments: this.remarks
      };

      try {
        const response = await instance.post('insert_review', requestData);
        if (response.data.message) {
          alert(response.data.message); // Alert the user that the review has been submitted
          this.$router.push({ name: 'customer_dashboard' });
        }
      } catch (error) {
        console.error('Error submitting remarks:', error);
      }
    }
  }
};
</script>

<style scoped>
.rating .diamond {
  font-size: 1.5em;
  color: #ff6666;
  cursor: pointer;
}

.rating .diamond.inactive {
  color: #ccc;
}
</style>
