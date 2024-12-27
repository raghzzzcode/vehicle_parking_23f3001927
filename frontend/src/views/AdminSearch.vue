<template>
  <div>
    <!-- Admin Navbar -->
    <AdminNavbar />

    <!-- Search Section -->
    <div class="container-fluid mb-5">
      <h3 class="text-center mb-4" style="color: #004aad; font-weight: 600;">Search</h3>

      <!-- Search Form -->
      <form @submit.prevent="submitSearch">
        <div class="row justify-content-center align-items-center">
          <div class="col-md-3">
            <div class="mb-3">
              <label for="searchBy" class="form-label" style="color: #004aad; font-weight: 500;">Search By:</label>
              <select v-model="searchBy" class="form-select" id="searchBy" name="searchBy" aria-label="Search By">
                <option value="services">Services</option>
                <option value="service_requests">Service Requests</option>
                <option value="customers">Customers</option>
                <option value="professionals">Professionals</option>
              </select>
            </div>
          </div>
          <div class="col-md-5">
            <div class="mb-3">
              <label for="searchText" class="form-label" style="color: #004aad; font-weight: 500;">Search Text:</label>
              <input
                type="text"
                class="form-control"
                id="searchText"
                v-model="searchText"
                placeholder="Enter search text (e.g., closed)"
                required
              />
            </div>
          </div>
          <div class="col-md-2 d-flex align-items-center">
            <button
              type="submit"
              class="btn"
              style="background-color: #004aad; color: white; border: none; height: 40px; width: 100%; font-weight: 600;"
            >
              Search
            </button>
          </div>
        </div>
      </form>

      <!-- Search Results Section -->
      <h3 class="text-center mb-3" style="color: #004aad; font-weight: 600;">{{ resultsTitle }}</h3>

      <!-- Search Results Table -->
      <div v-if="searchResults.length">
        <table class="table table-striped table-hover shadow rounded">
          <thead style="background-color: #d9eaf7; color: #084298;">
            <tr>
              <th v-if="searchBy === 'services' || searchBy === 'service_requests'">Service ID</th>
              <th v-if="searchBy === 'services'">Service Name</th>
              <th v-if="searchBy === 'services'">Base Price</th>
              <th v-if="searchBy === 'services'">Status</th>
              <th v-if="searchBy === 'service_requests'">Assigned Professional</th>
              <th v-if="searchBy === 'service_requests'">Requested Date</th>
              <th v-if="searchBy === 'service_requests'">Status (R/A/C)</th>
              <th v-if="searchBy === 'customers'">Customer Name</th>
              <th v-if="searchBy === 'customers'">Address</th>
              <th v-if="searchBy === 'customers'">Pincode</th>
              <th v-if="searchBy === 'professionals'">Professional Name</th>
              <th v-if="searchBy === 'professionals'">Experience</th>
              <th v-if="searchBy === 'professionals'">Service Provided</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(result, index) in searchResults" :key="index" style="background-color: #f9f9f9; color: #333;">
              <td v-if="searchBy === 'services' || searchBy === 'service_requests'">{{ result.service_id || 'N/A' }}</td>
              <td v-if="searchBy === 'services'">{{ result.service_name }}</td>
              <td v-if="searchBy === 'services'">${{ result.base_price }}</td>
              <td v-if="searchBy === 'services'">{{ result.status || 'N/A' }}</td>
              <td v-if="searchBy === 'service_requests'">{{ result.assigned_prof || 'N/A' }}</td>
              <td v-if="searchBy === 'service_requests'">{{ result.req_date }}</td>
              <td v-if="searchBy === 'service_requests'">{{ result.status || 'N/A' }}</td>
              <td v-if="searchBy === 'customers'">{{ result.full_name }}</td>
              <td v-if="searchBy === 'customers'">{{ result.address }}</td>
              <td v-if="searchBy === 'customers'">{{ result.pincode }}</td>
              <td v-if="searchBy === 'professionals'">{{ result.full_name }}</td>
              <td v-if="searchBy === 'professionals'">{{ result.experience }}</td>
              <td v-if="searchBy === 'professionals'">{{ result.service_name }}</td>
            </tr>
          </tbody>
        </table>

        <!-- Pagination Section -->
        <div class="d-flex justify-content-between align-items-center mt-4">
          <button
            class="btn btn-outline-primary"
            :disabled="currentPage === 1"
            @click="prevPage"
          >
            Previous
          </button>
          <p class="mb-0" style="color: #004aad; font-weight: 500;">
            Page {{ currentPage }} of {{ totalPages }}
          </p>
          <button
            class="btn btn-outline-primary"
            :disabled="currentPage === totalPages"
            @click="nextPage"
          >
            Next
          </button>
        </div>
      </div>
      <p v-else class="text-center" style="font-weight: 500; color: #888;">No results found for your search.</p>
    </div>

    <!-- App Footer -->
    <AppFooter />
  </div>
</template>

<script>
import instance from '@/axios.js';
import AdminNavbar from "@/components/AdminNavbar.vue";
import AppFooter from "@/components/AppFooter.vue";

export default {
  components: {
    AdminNavbar,
    AppFooter,
  },
  data() {
    return {
      searchBy: "services", // Default search option
      searchText: "",
      searchResults: [], // Will be fetched from the backend
      totalResults: 0,  // Store the total number of results
      currentPage: 1,   // Track the current page
      resultsPerPage: 10, // Default results per page
    };
  },
  computed: {
    resultsTitle() {
      if (this.searchBy === "services") {
        return "Services Search Results";
      } else if (this.searchBy === "service_requests") {
        return "Service Requests Search Results";
      } else if (this.searchBy === "customers") {
        return "Customers Search Results";
      } else if (this.searchBy === "professionals") {
        return "Professionals Search Results";
      }
      return "Search Results";
    },
    totalPages() {
      return Math.ceil(this.totalResults / this.resultsPerPage);
    },
  },
  methods: {
    async submitSearch() {
      try {
        const response = await instance.get("admin_search", {
          params: {
            by: this.searchBy,
            text: this.searchText,
            page: this.currentPage,  // Include pagination params
            per_page: this.resultsPerPage,
          },
        });
        this.searchResults = response.data.results;
        this.totalResults = response.data.total;  // Set the total results
      } catch (error) {
        console.error("Error fetching search results:", error);
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage += 1;
        this.submitSearch();
      }
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage -= 1;
        this.submitSearch();
      }
    },
  },
};
</script>

<style scoped>
/* Custom styling for the component */
</style>
