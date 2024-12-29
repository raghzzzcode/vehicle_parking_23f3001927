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
              <select
                class="form-select"
                v-model="searchBy"
                aria-label="Search By"
                style="background-color: #e9f2fb; color: #004aad;">
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
              <input
                type="text"
                class="form-control"
                v-model="searchText"
                placeholder="Enter search text"
                style="background-color: #e9f2fb; color: #004aad;">
            </div>
          </div>

          <div class="col-md-1 d-flex align-items-center">
            <button
              type="submit"
              class="btn"
              style="background-color: #004aad; color: white; border: none; height: 40px; margin-top: 15px;">
              Search
            </button>
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
import instance from '@/axios.js';
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
    async performSearch() {
      try {
        const professionalEmail = localStorage.getItem('professional_email'); // Fetch the email from localStorage

        if (!professionalEmail) {
          alert('Please log in first.');
          return;
        }

        const response = await instance.get('professional_search', {
          params: {
            professional_email: professionalEmail, // Pass the email as a parameter
            searchBy: this.searchBy,
            searchText: this.searchText,
          },
        });
        console.log(response.data);
        this.searchResults = response.data;
      } catch (error) {
        console.error('Error fetching search results:', error);
        // Display an error message to the user
        alert('An error occurred while fetching search results.');
      }
    },
  },
};
</script>

<style scoped>
/* You can add additional styles specific to this component here */
</style>
