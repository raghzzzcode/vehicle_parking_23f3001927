<template>
  <div class="container-fluid mb-5">
    <!-- Customer Navbar -->
    <CustomerNavbar />
  
    <!-- Main Content with Padding -->
    <div class="content-wrapper px-3">
      <!-- Search Form Section -->
      <form class="row align-items-center mb-4" @submit.prevent="search">
        <label for="searchBy" class="col-form-label me-2 search-label">Search by:</label>
        <div class="col-auto">
          <select v-model="searchBy" id="searchBy" class="form-select search-select">
            <option value="service_name">Service Name</option>
            <option value="pin_code">Pin Code</option>
            <option value="location">Location</option>
          </select>
        </div>
        <div class="col-auto">
          <input type="text" v-model="searchInput" class="form-control search-input" placeholder="Enter your search">
        </div>
        <div class="col-auto">
          <button type="submit" class="btn btn-primary search-btn">Search</button>
        </div>
      </form>
    
      <!-- Search Results Section -->
      <div class="mb-5">
        <h3 class="mb-4 text-center search-title">{{ searchTitle }}</h3>
    
        <div v-if="searchResults.length > 0">
          <table class="table table-striped table-hover shadow rounded search-table">
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
              <tr v-for="result in searchResults" :key="result.professional_id">
                <td>{{ result.full_name }}</td>
                <td>{{ result.service_name }}</td>
                <td>{{ result.experience }}</td>
                <td>{{ result.address }}</td>
                <td>{{ result.pincode }}</td>
                <td>
                  <form @submit.prevent="bookService(result.professional_id, result.service_name, result.full_name)">
                    <input type="hidden" :value="result.professional_id" />
                    <input type="hidden" :value="result.service_name" />
                    <input type="hidden" :value="result.full_name" />
                    <button type="submit" class="btn btn-success book-btn">Book</button>
                  </form>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
        <p v-else class="text-center no-results">No results found for your search.</p>
      </div>
    </div>
    
    <!-- App Footer -->
    <AppFooter />
  </div>
</template>

<script>
import CustomerNavbar from '@/components/CustomerNavbar.vue';
import AppFooter from '@/components/AppFooter.vue';
import instance from '@/axios.js';  // Assuming instance is configured for API requests

export default {
  components: {
    CustomerNavbar,
    AppFooter
  },
  data() {
    return {
      searchBy: 'service_name',
      searchInput: '',
      searchResults: []
    };
  },
  computed: {
    searchTitle() {
      if (this.searchBy === 'service_name') return 'Service Name Search Results';
      if (this.searchBy === 'pin_code') return 'Pincode Search Results';
      if (this.searchBy === 'location') return 'Location Search Results';
      return 'Search Results';
    }
  },
  methods: {
    // Search method to call the Flask API
    async search() {
      try {
        const response = await instance.get('/customer_search', {
          params: {
            search_by: this.searchBy,
            search_input: this.searchInput
          }
        });
        if (response.data.length > 0) {
          this.searchResults = response.data;
        } else {
          this.searchResults = [];
          alert('No results found.');
        }
      } catch (error) {
        console.error('Error fetching search results:', error);
        alert('An error occurred while searching.');
      }
    },

    // Booking method to call the Flask API
    async bookService(professional_id, service_name, professional_name) {
      const customer_id = 123; // Replace with actual customer ID from session or auth
      const data = {
        professional_id,
        service_name,
        professional_name,
        customer_id
      };

      try {
        const response = await instance.post('/customer_book', data);
        alert(response.data.message);  // Show success message
      } catch (error) {
        console.error('Error booking service:', error);
        alert('An error occurred while booking the service.');
      }
    }
  }
};
</script>

<style scoped>
/* Enhanced styling for search form and results */
.search-label {
  font-weight: 600;
  color: #004aad;
}

.search-select,
.search-input,
.search-btn {
  border-radius: 8px;
  font-size: 16px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.search-select,
.search-input {
  width: 250px;
}

.search-btn {
  padding: 10px 20px;
  font-weight: 600;
  background-color: #007bff;
  color: #fff;
  border: none;
}

.search-btn:hover {
  background-color: #0056b3;
}

.search-title {
  color: #004aad;
  font-weight: 600;
}

.search-table thead {
  background-color: #d9eaf7;
  color: #084298;
}

.search-table tbody tr {
  background-color: #f9f9f9;
  color: #333;
}

.book-btn {
  border-radius: 8px;
  padding: 8px 16px;
  font-weight: 600;
  background-color: #28a745;
  color: white;
  border: none;
}

.book-btn:hover {
  background-color: #218838;
}

.no-results {
  font-weight: 500;
  color: #888;
}

/* Padding adjustments for content wrapper */
.content-wrapper {
  padding-left: 15px;
  padding-right: 15px;
}

/* Navbar styling */
.navbar {
  width: 100%;
  background-color: #004aad;
  padding: 10px 0;
}

.navbar-nav .nav-link {
  color: white !important;
}

.navbar-nav .nav-link:hover {
  color: #ffbb33 !important;
}

/* App Footer - No additional padding */
.container-fluid {
  padding-left: 0;
  padding-right: 0;
}

/* Ensure full-width table responsiveness */
.table-responsive {
  width: 100%;
  overflow-x: auto;
}
</style>
