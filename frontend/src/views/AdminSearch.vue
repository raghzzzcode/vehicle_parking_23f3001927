<template>
  <div>
    <!-- Admin Navbar -->
    <AdminNavbar />

    <!-- Search Section -->
    <div class="container-fluid mb-5">
      <h3 class="text-center mb-4" style="color: #004aad; font-weight: 600;">Search</h3>

      <!-- Dynamic Search Instruction Message -->
      <p class="text-center" style="font-weight: 500; color: #888;">
        <span v-if="searchBy === 'services'">Services will be searched based on Service Name.</span>
        <span v-if="searchBy === 'service_requests'">Service Requests will be searched based on Service Status.</span>
        <span v-if="searchBy === 'customers'">Customers will be searched based on Full Name.</span>
        <span v-if="searchBy === 'professionals'">Professionals will be searched based on Full Name.</span>
      </p>

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
              <th v-if="searchBy === 'professionals'">Professional Name</th>
              <th v-if="searchBy === 'professionals'">Experience</th>
              <th v-if="searchBy === 'professionals'">Service Provided</th>
              <th v-if="searchBy === 'professionals'">Blocked Status</th>
              <th v-if="searchBy === 'professionals'">Action</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="(result, index) in searchResults"
              :key="index"
              style="background-color: #f9f9f9; color: #333;"
            >
              <td v-if="searchBy === 'professionals'">{{ result.professional_name }}</td>
              <td v-if="searchBy === 'professionals'">{{ result.experience }}</td>
              <td v-if="searchBy === 'professionals'">{{ result.service_provided }}</td>
              <td v-if="searchBy === 'professionals'">
                {{ result.is_blocked ? "Blocked" : "Unblocked" }}
              </td>
              <td v-if="searchBy === 'professionals'">
                <button
                  @click="toggleBlock(result.professional_id)"
                  class="btn"
                  :class="result.is_blocked ? 'btn-danger' : 'btn-success'"
                >
                  {{ result.is_blocked ? "Unblock" : "Block" }}
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <p v-else class="text-center" style="font-weight: 500; color: #888;">No results found for your search.</p>
    </div>

    <!-- App Footer -->
    <AppFooter />
  </div>
</template>

<script>
import instance from "@/axios.js";
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
  },
  methods: {
    async submitSearch() {
      try {
        const response = await instance.get("admin_search", {
          params: {
            by: this.searchBy,
            text: this.searchText,
          },
        });
        this.searchResults = response.data.results;

        // Fetch blocked status for professionals
        if (this.searchBy === "professionals" && this.searchResults.length) {
          await this.fetchBlockedStatus();
        }
      } catch (error) {
        console.error("Error fetching search results:", error);
      }
    },
    async fetchBlockedStatus() {
      try {
        const promises = this.searchResults.map(async (professional) => {
          const response = await instance.get("get_blocked_or_not", {
            params: { professional_id: professional.professional_id },
          });
          professional.is_blocked = response.data.blocked_or_not;
        });
        await Promise.all(promises);
      } catch (error) {
        console.error("Error fetching blocked status:", error);
      }
    },
    async toggleBlock(professionalId) {
      try {
        const professional = this.searchResults.find(
          (p) => p.professional_id === professionalId
        );
        const action = professional.is_blocked ? "unblock" : "block";

        await instance.patch("change_blocking_status", {
          professional_id: professionalId,
          action,
        });

        // Update the blocked status
        professional.is_blocked = !professional.is_blocked;
      } catch (error) {
        console.error("Error toggling block status:", error);
      }
    },
  },
  watch: {
    searchBy() {
      // Reset the search results and search text when searchBy changes
      this.searchResults = [];
      this.searchText = "";
    },
  },
};
</script>

<style scoped>
/* Custom styling for the component */
</style>
