<script setup>
import { ref, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth"

const route = useRoute()
const router = useRouter()
const authstore = useAuthStore()

const applications = ref([])
const error = ref(null)
const loading = ref(true)

const fetchapplications = async () => {
  error.value = null
  loading.value = true

  try {
    const response = await fetch(
      `http://localhost:5000/api/company/drive/${route.params.drive_id}/applications`,
      {
        headers: {
          "Authentication-Token": authstore.token
        }
      }
    )

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.message || "The applications could not be fetched.")
    }

    applications.value = data
  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchapplications()
})

const goToApplicationDetails = (application) => {
  router.push(`/company/application/${application.application_id}`)
}
</script>

<template>
  <div class="container mt-4">

    <div v-if="error" class="alert alert-danger">
      {{ error }}
    </div>

    <div v-else-if="loading" class="text-center">
      <p>Loading applications...</p>
    </div>

    <div v-else-if="applications.length === 0" class="text-center mt-5">
      <h4>No Applications Yet</h4>
      <p class="text-muted">Students have not applied to this drive.</p>
    </div>

    <div v-else class="row">
      <div
        class="col-md-6 col-lg-4 mb-4"
        v-for="application in applications"
        :key="application.application_id"
      >
        <div class="card h-100 shadow-sm">
          <div class="card-body">

            <h4 class="card-title">{{ application.student_name }}</h4>

            <p class="text-muted">
              Application ID: {{ application.application_id }}
            </p>

            <h6>Roll Number: {{ application.roll_number }}</h6>

            <ul class="list-group list-group-flush mb-3">
              <li class="list-group-item">
                <strong>Status:</strong>
                <span
                  class="badge"
                  :class="{
                    'bg-secondary': application.status === 'APPLIED',
                    'bg-warning': application.status === 'SHORTLISTED',
                    'bg-success': application.status === 'SELECTED',
                    'bg-danger': application.status === 'REJECTED'
                  }"
                >
                  {{ application.status }}
                </span>
              </li>
            </ul>

            <button
              class="btn btn-primary"
              @click="goToApplicationDetails(application)"
            >
              View Application
            </button>

          </div>
        </div>
      </div>
    </div>

  </div>
</template>