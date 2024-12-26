<template>
    <div>
      <!-- Customer Navbar -->
      <CustomerNavbar />
  
      <!-- Service Remarks Form Section -->
      <div class="container-fluid mb-5" style="max-width: 600px; margin-top: 30px;">
        <form @submit.prevent="submitRemarks" class="shadow p-4 rounded" style="border: 2px solid #ccc; background-color: #f9f9f9;">
          <h4 class="text-center text-primary mb-3">Service Remarks</h4>
          <p class="text-center text-primary">Service ID: {{ service.service_id }}</p>
  
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
  
  export default {
    name: "CustomerRemarks",
    components: {
      CustomerNavbar,
      AppFooter
    },
    data() {
      return {
        service: {
          service_id: 12345,
          service_name: "Plumbing",
          professional_name: "John Doe"
        },
        diamonds: [0, 1, 2, 3, 4], // Representing 5 rating diamonds
        rating: 3, // Default rating
        remarks: "" // Remarks entered by the user
      };
    },
    methods: {
      setRating(index) {
        this.rating = index + 1;
      },
      submitRemarks() {
        // Simulate form submission
        alert(`Service ID: ${this.service.service_id}\nRating: ${this.rating}\nRemarks: ${this.remarks}`);
        // Normally, you'd submit to the server here
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
  