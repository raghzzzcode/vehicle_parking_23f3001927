import { createRouter, createWebHistory } from 'vue-router';
import BaseLayout from '@/layout/BaseLayout.vue';
import AllLogin from '@/views/AllLogin.vue';
import CustomerRegister from '@/views/CustomerRegister.vue';
import ProfessionalRegister from '@/views/ProfessionalRegister.vue';
import CustomerDashboard from '@/views/CustomerDashboard.vue';
import CustomerProfile from '@/views/CustomerProfile.vue';
import CustomerRemarks from '@/views/CustomerRemarks.vue';
import CustomerSearch from '@/views/CustomerSearch.vue';    
import CustomerSummary from '@/views/CustomerSummary.vue';
import ProfessionalDashboard from '@/views/ProfessionalDashboard.vue';
import ProfessionalEditProfile from '@/views/ProfessionalEditProfile.vue';
import ProfessionalSearch from '@/views/ProfessionalSearch.vue';
import ProfessionalSummary from '@/views/ProfessionalSummary.vue';
import ProfessionalViewProfile from '@/views/ProfessionalViewProfile.vue';
import AdminAddService from '@/views/AdminAddService.vue';
import AdminDashboard from '@/views/AdminDashboard.vue';
import AdminEditService from '@/views/AdminEditService.vue';
import AdminSearch from '@/views/AdminSearch.vue';
import AdminSummary from '@/views/AdminSummary.vue';


const routes = [
  {
    path: '/',
    name: 'home',
    component: BaseLayout,
  },
  {
    path: '/alllogin',
    name: 'login',
    component: AllLogin
  },
  {
    path: '/customer_register',
    name: 'customer_register',
    component: CustomerRegister
  },
  {
    path: '/professional_register',
    name: 'professional_register',
    component: ProfessionalRegister
  },
  {
    path: '/customer_dashboard',
    name: 'customer_dashboard',
    component: CustomerDashboard
  },
  {
    path: '/customer_profile',
    name: 'customer_profile',
    component: CustomerProfile
  },
  {
    path: '/customer_remarks',
    name: 'customer_remarks',
    component: CustomerRemarks
  },
  {
    path: '/customer_search',
    name: 'customer_search',
    component: CustomerSearch
  },
  {
    path: '/customer_summary',
    name: 'customer_summary',
    component: CustomerSummary
  },
  {
    path: '/professional_dashboard',
    name: 'professional_dashboard',
    component: ProfessionalDashboard
  },
  {
    path: '/professional_edit_profile',
    name: 'professional_edit_profile',
    component: ProfessionalEditProfile
  },
  {
    path: '/professional_search',
    name: 'professional_search',
    component: ProfessionalSearch
  },
  {
    path: '/professional_summary',
    name: 'professional_summary',
    component: ProfessionalSummary
  },
  {
    path: '/professional_view_profile',
    name: 'professional_view_profile',
    component: ProfessionalViewProfile
  },
  {
    path: '/logout',
    name: 'logout',
    component: AllLogin
  },
  {
    path: '/admin_add_service',
    name: 'admin_add_service',
    component: AdminAddService
  },
  {
    path: '/admin_dashboard',
    name: 'admin_dashboard',
    component: AdminDashboard
  },
  {
    path: '/admin_edit_service/:id',
    name: 'admin_edit_service',
    component: AdminEditService
  },
  {
    path: '/admin_search',
    name: 'admin_search',
    component: AdminSearch
  },
  {
    path: '/admin_summary',
    name: 'admin_summary',
    component: AdminSummary
  }

];

// Create a router instance
const router = createRouter({
    history: createWebHistory(),
    routes,
  });
  
export default router;