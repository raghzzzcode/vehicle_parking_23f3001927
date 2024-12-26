<template>
    <div>
      <!-- Customer Navbar -->
      <CustomerNavbar />
  
      <!-- Profile Content -->
      <div class="d-flex justify-content-center align-items-center" style="min-height: 80vh;">
        <div class="p-4 shadow-lg rounded"
          style="max-width: 400px; width: 100%; background: linear-gradient(to bottom, #0066cc, #004aad); color: #ffffff;">
          <h2 class="text-center mb-4" style="color: #ffffff;">Customer Profile</h2>
          <form>
            <div class="mb-3">
              <label for="email" class="form-label">Email ID (Username)</label>
              <input type="email" class="form-control" id="email" name="email" v-model="customer.email" readonly
                style="border: none; background-color: #e0f0ff;">
            </div>
            <div class="mb-3">
              <label for="fullname" class="form-label">Fullname</label>
              <input type="text" class="form-control" id="fullname" name="fullname" v-model="customer.fullName"
                readonly style="border: none; background-color: #e0f0ff;">
            </div>
            <div class="mb-3">
              <label for="address" class="form-label">Address</label>
              <input type="text" class="form-control" id="address" name="address" v-model="customer.address" readonly
                style="border: none; background-color: #e0f0ff;">
            </div>
            <div class="mb-3">
              <label for="pincode" class="form-label">Pincode</label>
              <input type="text" class="form-control" id="pincode" name="pincode" v-model="customer.pincode" readonly
                style="border: none; background-color: #e0f0ff;">
            </div>
            <div class="d-flex justify-content-center mt-4">
              <button type="button" class="btn btn-danger" @click="logout">Logout</button>
            </div>
          </form>
        </div>
      </div>
  
      <!-- App Footer -->
      <AppFooter />
    </div>
  </template>
  
  <script>
  // Importing CustomerNavbar and AppFooter components
    import CustomerNavbar from "@/components/CustomerNavbar.vue";
    import AppFooter from "@/components/AppFooter.vue";  
  export default {
    components: {
      CustomerNavbar,
      AppFooter
    },
    data() {
      return {
        customer: {
          email: "customer@example.com",  // Example email
          fullName: "John Doe",           // Example full name
          address: "123 Main St, City",   // Example address
          pincode: "123456"               // Example pincode
        }
      };
    },
    methods: {
      logout() {
        // Handle logout functionality, for now it's a placeholder
        console.log("Logging out...");
        // Redirect to login page or clear session here
        this.$router.push('/login');
      }
    }
  };
  </script>
  
  <style scoped>
  /* Styles specific to this component */
  .form-label {
    font-weight: bold;
  }
  
  .form-control {
    font-size: 14px;
  }
  
  .btn-danger {
    background-color: #dc3545;
    color: white;
    border: none;
    border-radius: 5px;
    padding: 8px 12px;
    transition: background-color 0.3s;
  }
  
  .btn-danger:hover {
    background-color: #c82333;
  }
  </style>
  