<script setup>
import { ref, onMounted, watch } from "vue"
import { useRoute } from "vue-router"
import { useAuthStore } from "@/stores/auth"

const route = useRoute()
const authstore = useAuthStore()
const drives = ref([])
const loading = ref(false)
const error = ref(null)

const fetchDrives = async (status) => {
  if (!status) return
  error.value=false
  loading.value = true

  try {
    const response = await fetch(`http://localhost:5000/api/company/drives?status=${status}`, {
      headers: {
        "Authentication-Token": authstore.token
      }
    })
    const data = await response.json()
    if (!response.ok) {
      throw new Error(data.message||"Failed to fetch drives")
    }

    drives.value = data

  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchDrives(route.query.status)
})

watch(
  () => route.query.status,
  (newStatus) => {
    fetchDrives(newStatus)
  }
)
</script>

<template>
  <div class="container mt-4">

    <div class="d-flex justify-content-between align-items-center mb-4">
      <h3 class="mb-0 text-capitalize">
        {{ route.query.status }} Drives
      </h3>
    </div>

   
    <div v-if="loading" class="alert alert-info">
      Loading drives...
    </div>

  
    <div v-if="error" class="alert alert-danger">
      {{ error }}
    </div>

 
    <div v-if="!loading && drives.length === 0" class="alert alert-warning">
      No drives found.
    </div>

    
    <div class="row">
      <div
        class="col-md-6 col-lg-4 mb-4"
        v-for="drive in drives"
        :key="drive.drive_id"
      >
        <div class="card h-100 shadow-sm">
          <div class="card-body">
            <h5 class="card-title">{{ drive.title }}</h5>
            <p>{{ drive.drive_id }}</p>

            <ul class="list-group list-group-flush mb-3">
              <li class="list-group-item">
                <strong>Status:</strong>
                <span class="badge bg-secondary text-capitalize">
                  {{ drive.status }}
                </span>
              </li>
            </ul>
           <RouterLink class="btn btn-primary" :to="`/company/drives/${drive.drive_id}`" role="button">View Details</RouterLink>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>