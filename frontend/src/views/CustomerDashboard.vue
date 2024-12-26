<template>
    <div>
      <!-- Customer Navbar -->
      <CustomerNavbar />
  
      <div class="container-fluid mb-5">
        <!-- Service Options Section -->
        <h3 class="text-center mb-4" style="color: #004aad; font-weight: bold;">Looking For</h3>
        <div class="row text-center mb-5">
          <div v-for="(service, index) in services" :key="index" class="col-md-3 mb-3">
            <button type="button" class="service-btn" @click="selectService(service)">
              <p>{{ service.name }}</p>
            </button>
          </div>
        </div>
  
        <!-- Search Results and Other Sections -->
        <div v-if="searchResults.length > 0">
          <h3 class="text-center mb-4" style="color: #004aad; font-weight: bold;">Professionals</h3>
          <table class="table table-striped table-hover shadow rounded">
            <thead>
              <tr>
                <th>Professional Name</th>
                <th>Service Name</th>
                <th>Experience</th>
                <th>Address</th>
                <th>Pincode</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(result, index) in searchResults" :key="index">
                <td>{{ result.professionalName }}</td>
                <td>{{ result.serviceName }}</td>
                <td>{{ result.experience }} years</td>
                <td>{{ result.address }}</td>
                <td>{{ result.pincode }}</td>
                <td>
                  <button @click="bookService(result)" class="btn btn-success">Book</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <div v-else>
          <p class="text-center">Select a service to view available professionals.</p>
        </div>
  
        <!-- Service History Section -->
        <div class="container-fluid">
          <div class="mb-5">
            <h3 class="text-center mb-3" style="color: #004aad; font-weight: bold;">Service History</h3>
            <table class="table table-striped table-hover shadow rounded">
              <thead>
                <tr>
                  <th>Service Name</th>
                  <th>Professional Name</th>
                  <th>Email</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(service, index) in serviceHistory" :key="index">
                  <td>{{ service.serviceName }}</td>
                  <td>{{ service.professionalName }}</td>
                  <td>{{ service.email }}</td>
                  <td>
                    <button v-if="service.status !== 'Closed'" @click="closeService(service)" class="btn btn-danger">Close</button>
                    <span v-else>Closed</span>
                  </td>
                </tr>
                <tr v-if="serviceHistory.length === 0">
                  <td colspan="4" class="text-center">No service history.</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
  
      <!-- App Footer -->
      <AppFooter />
    </div>
  </template>
  
  <script>
  import CustomerNavbar from "@/components/CustomerNavbar.vue";
  import AppFooter from "@/components/AppFooter.vue";
  
  export default {
    name: "CustomerDashboard",
    components: {
      CustomerNavbar,
      AppFooter,
    },
    data() {
      return {
        services: [
          { name: "Plumbing" },
          { name: "Electrical" },
          { name: "Carpentry" },
          { name: "Cleaning" },
        ],
        searchResults: [
          { professionalName: "John Doe", serviceName: "Plumbing", experience: 5, address: "123 Main St", pincode: "123456", email: "johndoe@example.com" },
          { professionalName: "Jane Smith", serviceName: "Electrical", experience: 8, address: "456 Elm St", pincode: "654321", email: "janesmith@example.com" },
          { professionalName: "Bob Johnson", serviceName: "Carpentry", experience: 4, address: "789 Oak St", pincode: "112233", email: "bobjohnson@example.com" },
        ],
        serviceHistory: [
          { serviceName: "Plumbing", professionalName: "John Doe", email: "johndoe@example.com", status: "Closed" },
          { serviceName: "Cleaning", professionalName: "Mary Ann", email: "maryann@example.com", status: "Pending" },
        ],
      };
    },
    methods: {
      selectService(service) {
        // Simulate a search for professionals based on the selected service
        console.log(`Searching for professionals for ${service.name}...`);
        // You can update the `searchResults` with actual API calls here
      },
      bookService(result) {
        // Simulate booking a service
        alert(`Service booked with ${result.professionalName}`);
      },
      closeService(service) {
        // Simulate closing a service
        service.status = "Closed";
        alert(`Service for ${service.serviceName} closed.`);
      },
    },
  };
  </script>
  
  <style scoped>
  /* Styling for the service selection buttons */
  .service-btn {
    display: block;
    background-color: #007bff;
    color: white;
    border: none;
    padding: 12px 24px;
    font-size: 16px;
    border-radius: 8px;
    width: 100%;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s, box-shadow 0.3s;
  }
  
  .service-btn:hover {
    transform: scale(1.05);
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
  }
  
  .service-btn p {
    margin: 0;
  }
  
  /* Styling for the tables */
  .table {
    background-color: #ffffff;
    border-radius: 10px;
  }
  
  .table th, .table td {
    text-align: center;
    padding: 15px;
  }
  
  .table-striped tbody tr:nth-of-type(odd) {
    background-color: #f9f9f9;
  }
  
  .table-hover tbody tr:hover {
    background-color: #f1f1f1;
  }
  
  /* Button styles */
  .btn-success {
    background-color: #28a745;
    color: white;
    border-radius: 5px;
    padding: 8px 16px;
    transition: background-color 0.3s;
  }
  
  .btn-success:hover {
    background-color: #218838;
  }
  
  .btn-danger {
    background-color: #dc3545;
    color: white;
    border-radius: 5px;
    padding: 8px 16px;
    transition: background-color 0.3s;
  }
  
  .btn-danger:hover {
    background-color: #c82333;
  }
  </style>
  