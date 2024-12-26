<template>
    <div>
      <ProfessionalNavbar />
      <!-- Search Section -->
      <div class="container mb-5">
        <h3 class="text-center mb-3" style="color: #004aad;">Search</h3>
  
        <!-- Search Form -->
        <form @submit.prevent="performSearch">
          <div class="row justify-content-center">
            <div class="col-md-4">
              <div class="mb-3">
                <label for="searchBy" class="form-label" style="color: #004aad;">Search By:</label>
                <select class="form-select" v-model="searchBy" aria-label="Search By" style="background-color: #e9f2fb; color: #004aad;">
                  <option value="date">Date</option>
                  <option value="location">Location</option>
                  <option value="pincode">Pincode</option>
                  <option value="customer">Customer Name</option>
                </select>
              </div>
            </div>
            <div class="col-md-4">
              <div class="mb-3">
                <label for="searchText" class="form-label" style="color: #004aad;">Search Text:</label>
                <input type="text" class="form-control" v-model="searchText" placeholder="Enter search text" style="background-color: #e9f2fb; color: #004aad;">
              </div>
            </div>
            <div class="col-md-1 d-flex align-items-center">
              <button type="submit" class="btn" style="background-color: #004aad; color: white; border: none; height: 40px; margin-top: 15px;">Search</button>
            </div>
          </div>
        </form>
      </div>
  
      <!-- Search Results Section -->
      <div v-if="searchResults.length > 0" class="container-fluid">
        <h3 class="text-center mb-3" style="color: #004aad;">Search Results</h3>
        <table class="table table-striped table-hover shadow rounded" style="background-color: #f0f8ff;">
          <thead style="background-color: #cfe2ff; color: #084298;">
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
            <tr v-for="(service, index) in searchResults" :key="index">
              <td>{{ service.id }}</td>
              <td>{{ service.customer_name }}</td>
              <td>{{ service.email }}</td>
              <td>{{ service.location }}</td>
              <td>{{ service.date }}</td>
              <td>
                <span v-if="service.rating">
                  {{ '⭐'.repeat(service.rating) }}
                </span>
                <span v-else>No rating</span>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
  
      <!-- No Results Section -->
      <div v-else class="text-center mt-4">
        <p style="color: #004aad;">No results found for your search.</p>
      </div>
  
      <AppFooter />
    </div>
  </template>
  
  <script>
    import ProfessionalNavbar from '@/components/ProfessionalNavbar.vue';
    import AppFooter from '@/components/AppFooter.vue';
  
  export default {
    components: {
      ProfessionalNavbar,
      AppFooter,
    },
    data() {
      return {
        searchBy: 'date', // Default search by "date"
        searchText: '',
        searchResults: [], // This will store search results
      };
    },
    methods: {
      performSearch() {
        // Simulated search data (you would replace this with an API call)
        const sampleResults = [
          {
            id: 1,
            customer_name: 'John Doe',
            email: 'john.doe@example.com',
            location: 'New York',
            date: '2024-12-25',
            rating: 5,
          },
          {
            id: 2,
            customer_name: 'Jane Smith',
            email: 'jane.smith@example.com',
            location: 'Los Angeles',
            date: '2024-12-24',
            rating: 4,
          },
        ];
  
        // Filter search results based on the search criteria
        this.searchResults = sampleResults.filter((service) => {
          if (this.searchBy === 'date') {
            return service.date.includes(this.searchText);
          } else if (this.searchBy === 'location') {
            return service.location.toLowerCase().includes(this.searchText.toLowerCase());
          } else if (this.searchBy === 'pincode') {
            return service.pincode && service.pincode.includes(this.searchText);
          } else if (this.searchBy === 'customer') {
            return service.customer_name.toLowerCase().includes(this.searchText.toLowerCase());
          }
          return false;
        });
      },
    },
  };
  </script>
  
  <style scoped>
  /* You can add additional styles specific to this component here */
  </style>
  