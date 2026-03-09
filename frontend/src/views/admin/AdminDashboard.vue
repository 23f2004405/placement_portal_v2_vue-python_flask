<script setup>
import { ref, onMounted } from "vue"
import { useAuthStore } from "@/stores/auth"

const authstore = useAuthStore()

const error = ref(null)
const details = ref({})
const loading = ref(true)

const fetchdetails = async () => {
  error.value = null
  loading.value = true

  try {
    const response = await fetch(
      "http://localhost:5000/api/admin/dashboard",
      {
        headers: {
          "Authentication-Token": authstore.token
        }
      }
    )

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.message || "Cannot fetch details")
    }

    details.value = data
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchdetails()
})
</script>

<template>
<div class="container mt-5">

  <div class="card shadow">

    <div class="card-header bg-dark text-white">
      Admin Profile
    </div>

    <div class="card-body">

      <div v-if="loading" class="text-center">
        Loading...
      </div>

      <div v-else>

        <div v-if="error" class="alert alert-danger">
          {{ error }}
        </div>

        <div v-else>

          <div class="row mb-3">
            <div class="col-md-6">
              <strong>Student Count:</strong>
              <p>{{ details.total_students }}</p>
            </div>

            <div class="col-md-6">
              <strong>Approved Company Count:</strong>
              <p>{{ details.approved_companies }}</p>
            </div>
          </div>

          <div class="row mb-3">
            <div class="col-md-6">
              <strong>Pending Approval Company Count:</strong>
              <p>{{ details.pending_companies }}</p>
            </div>

            <div class="col-md-6">
              <strong>Placement Drives Count:</strong>
              <p>{{ details.total_placement_drives }}</p>
            </div>
          </div>

        </div>

      </div>

    </div>
  </div>

</div>
</template>