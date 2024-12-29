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
import instance from '@/axios.js';
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
        email: '',
        fullName: '',
        address: '',
        pincode: ''
      }
    };
  },
  mounted() {
    this.fetchCustomerProfile();
  },
  methods: {
    async fetchCustomerProfile() {
  try {
    const email = localStorage.getItem('customer_email');
    if (!email) {
      console.error('Customer email not found in localStorage.');
      return;
    }
    
    const response = await instance.get(`customer/profile?customer_email=${email}`);
    this.customer = {
      email: response.data.email || '',
      fullName: response.data.full_name || '',
      address: response.data.address || '',
      pincode: response.data.pincode || ''
    };
  } catch (error) {
    console.error("Error fetching customer profile:", error);
  }
},
async logout() {
  try {
    await instance.post('logout'); // Perform the logout API call
    this.$router.push('/logout'); // Navigate to the 'logout' route
  } catch (error) {
    console.error("Logout error:", error);
  }
}
  }
};
</script>
