<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
    <div class="container">

      <RouterLink class="navbar-brand" to="/">Placement Portal</RouterLink>

      <div class="collapse navbar-collapse">
        <ul class="navbar-nav ms-auto">

          <!-- anonymous -->
          <template v-if="!authstore.isAuthenticated">
            <li class="nav-item">
              <RouterLink class="nav-link" to="/register_student">
                Register Student
              </RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink class="nav-link" to="/register_company">
                Register Company
              </RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink class="nav-link" to="/login">
                Login
              </RouterLink>
            </li>
          </template>

          <!-- Company -->
          <template v-else-if="authstore.role === 'COMPANY'">
            <li class="nav-item">
              <RouterLink class="nav-link" :to="{name:'company_dashboard',params:{company_id:authstore.role_based_id}}">
                Dashboard
              </RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink class="nav-link" to="/company/create_drive">
              Create Drive
              </RouterLink>
            </li>
  <li class="nav-item dropdown">
    <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">Placement Drives</a>

    <ul class="dropdown-menu">
      <li>
        <RouterLink class="dropdown-item" :to="{ path: '/company/drives', query: { status: 'APPROVED' } }">
        Approved
        </RouterLink>
      </li>

      <li>
        <RouterLink class="dropdown-item" :to="{ path: '/company/drives', query: { status: 'PENDING' } }">
        Pending
        </RouterLink>
      </li>

      <li>
        <RouterLink class="dropdown-item" :to="{ path: '/company/drives', query: { status: 'CLOSED' } }">
        Closed
        </RouterLink>
      </li>
    </ul>
  </li>

            <li class="nav-item">
              <button class="btn btn-danger btn-sm ms-2" @click="logout">
                Logout
              </button>
            </li>
          </template>

          <!--  Student -->
          <template v-else-if="authstore.role === 'STUDENT'">
            <li class="nav-item">
              <RouterLink class="nav-link" :to="{name:'student_dashboard',params:{student_id:authstore.role_based_id}}">
                Dashboard
              </RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink class="nav-link" to="/student/apply_drives">
                Apply for Drives
              </RouterLink>
            </li>

  <li class="nav-item dropdown">
    <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown">Application History</a>

    <ul class="dropdown-menu">
      <li>
        <RouterLink class="dropdown-item" :to="{ path: '/student/history/applications', query: { status: 'APPLIED' } }">
        Applied
        </RouterLink>
      </li>

      <li>
        <RouterLink class="dropdown-item" :to="{ path: '/student/history/applications', query: { status: 'REJECTED' } }">
        Rejected
        </RouterLink>
      </li>

      <li>
        <RouterLink class="dropdown-item" :to="{ path: '/student/history/applications', query: { status: 'SHORTLISTED' } }">
        Shortlisted
        </RouterLink>
      </li>

      <li>
        <RouterLink class="dropdown-item" :to="{ path: '/student/history/applications', query: { status: 'SELECTED' } }">
        Selected
        </RouterLink>
      </li>
    </ul>
  </li>
            <li class="nav-item">
              <RouterLink class="nav-link" to="/student/edit_profile">
                Edit Profile
              </RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink class="nav-link" to="/student/upload_resume">
                Upload Resume
              </RouterLink>
            </li>

            <li class="nav-item">
              <button class="btn btn-danger btn-sm ms-2" @click="logout">
                Logout
              </button>
            </li>
          </template>

          <!-- Admin -->
          <template v-else-if="authstore.role === 'ADMIN'">
            <li class="nav-item">
              <RouterLink class="nav-link" to="/admin/dashboard">
                Admin Panel
              </RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink class="nav-link" to="/admin/companies">
                Companies
              </RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink class="nav-link" to="/admin/students">
                Students
              </RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink class="nav-link" to="/admin/company/registrations">
                Company Registrations
              </RouterLink>
            </li>

            <li class="nav-item">
              <RouterLink class="nav-link" to="/admin/drives">
                Placement Drives
              </RouterLink>
            </li>


            <li class="nav-item">
              <button class="btn btn-danger btn-sm ms-2" @click="logout">
                Logout
              </button>
            </li>
          </template>

        </ul>
      </div>

    </div>
  </nav>
  <router-view />
</template>

<script setup>
import { useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth"

const router = useRouter()
const authstore = useAuthStore()

async function logout() {
try {
    await fetch("http://localhost:5000/api/logout", {
      method: "POST",
      headers: {
        "Authentication-Token": authstore.token
      }
    })

    await authstore.logout()   
    router.push("/login")

  } catch (error) {
    console.error("Logout failed:", error)
  }
}
</script>