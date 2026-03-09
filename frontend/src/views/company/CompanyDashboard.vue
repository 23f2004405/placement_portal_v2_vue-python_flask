<template>
  <div class="container mt-5">

    <div class="card shadow">
      <div class="card-header bg-dark text-white">
        Company Profile
      </div>

      <div class="card-body">

        <div v-if="loading" class="text-center">
          Loading...
        </div>

        <div v-else-if="error" class="alert alert-danger">
          {{ error }}
        </div>

        <div v-else>

          <div class="row mb-3">
            <div class="col-md-6">
              <strong>Company Name:</strong>
              <p>{{ company.company_name }}</p>
            </div>

            <div class="col-md-6">
              <strong>HR Contact:</strong>
              <p>{{ company.hr_contact }}</p>
            </div>
          </div>

          <div class="row mb-3">
            <div class="col-md-6">
              <strong>Website:</strong>
              <p>{{ company.website }}</p>
            </div>

            <div class="col-md-6">
              <strong>Username:</strong>
              <p>{{ company.username }}</p>
            </div>
          </div>

          <div class="row mb-3">
            <div class="col-md-6">
              <strong>Email:</strong>
              <p>{{ company.email }}</p>
            </div>

            <div class="col-md-6">
              <strong>Approval Status:</strong>
              <span 
                class="badge"
                :class="company.approval_status === 'APPROVED' 
                        ? 'bg-success' 
                        : 'bg-warning text-dark'"
              >
                {{ company.approval_status }}
              </span>
            </div>
          </div>

          <div v-if="company.approval_status !== 'APPROVED'" 
               class="alert alert-warning mt-3">
            Your company account is not approved yet. 
            You cannot create placement drives until approval.
          </div>

        </div>

      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { useRoute } from "vue-router"
import { useAuthStore } from "@/stores/auth"

const route = useRoute()
const authStore = useAuthStore()

const company = ref({})
const loading = ref(null)
const error = ref(null)

const fetchcompany=async () => {
  error.value=false
  loading.value=true
  try {
    const response = await fetch(
      `http://localhost:5000/api/company/${route.params.company_id}`,
      {
        headers: {
          "Authentication-Token": authStore.token
        }
      }
    )

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.message || "Failed to fetch company details")
    }

    company.value = data

  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}
onMounted(()=>{
  fetchcompany()
})
</script>