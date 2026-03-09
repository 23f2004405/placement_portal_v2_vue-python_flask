<script setup>
import { onMounted, ref } from "vue"
import { useAuthStore } from "@/stores/auth"
import { useRouter } from "vue-router"

const drives = ref([])
const loading = ref(false)
const error = ref(null)
const router =useRouter()
const authstore=useAuthStore()

const filters = ref({
  cgpa: null,
  company_name: "",
  year: null,
  drive_id: null
})

const createqueryparams = () => {
  const params = new URLSearchParams()

  Object.entries(filters.value).forEach(([key,value])=>{
    if (typeof value === 'string'){
      value=value.trim()
    }
    if (value != "" && value != null && value != undefined){
      params.append(key,value)
    }
  })
  return params.toString()
}

const fetchDrives = async () => {
  loading.value = true
  error.value = null
  drives.value = []

  try {
    const query = createqueryparams()
    const response = await fetch(
      `http://localhost:5000/api/student/approved_drives?${query}`,
      {
        headers: {
          'Authentication-Token': authstore.token
        }
      }
    )
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

const resetFilters = async () => {
  filters.value = {
    cgpa: null,
    company_name: "",
    year: null,
    drive_id: null
  }
  await fetchDrives()
}

const gotoDriveDetails =(drive)=>{
  router.push(`/student/drive/${drive.drive_id}`)
}
onMounted(()=>{
  fetchDrives()
})
</script>

<style scoped>
.card {
  border-radius: 10px;
}
</style>


<template>
  <div class="container mt-4">
    <h2 class="mb-4">Approved Placement Drives</h2>

    <div class="card p-3 mb-4">
      <div class="row g-3">
        <div class="col-md-3">
          <label class="form-label">CGPA</label>
          <input
            v-model.number="filters.cgpa"
            type="number"
            step="0.01"
            min="0"
            max="10"
            class="form-control"
          />
        </div>

        <div class="col-md-3">
          <label class="form-label">Company Name</label>
          <input
            v-model="filters.company_name"
            type="text"
            class="form-control"
          />
        </div>

        <div class="col-md-3">
          <label class="form-label">Passing Year</label>
          <input
            v-model.number="filters.year"
            type="number"
            class="form-control"
          />
        </div>

        <div class="col-md-3">
          <label class="form-label">Drive ID</label>
          <input
            v-model.number="filters.drive_id"
            type="number"
            class="form-control"
          />
        </div>
      </div>

      <div class="mt-3">
        <button class="btn btn-primary me-2" @click="fetchDrives">
          Search
        </button>
        <button class="btn btn-secondary" @click="resetFilters">
          Reset
        </button>
      </div>
    </div>

   
    <div v-if="loading" class="text-center">
      <div class="spinner-border"></div>
      <p>Loading...</p>
    </div>

    
    <div v-if="error" class="alert alert-danger">
      {{ error }}
    </div>

    <div v-if="!loading && drives.length === 0" class="text-muted">
      No drives found.
    </div>

    <div class="row">
      <div
        class="col-md-4 mb-3"
        v-for="drive in drives"
        :key="drive.drive_id"
      >
        <div class="card h-100">
          <div class="card-body">
            <h5 class="card-title">{{ drive.title }}</h5>
            <p class="card-text">
              <strong>Company:</strong> {{ drive.company_name }} <br />
              <strong>Drive ID:</strong> {{ drive.drive_id }} <br />
              <strong>Deadline:</strong>
              {{ drive.application_deadline }}
            </p>
            <button class="btn btn-primary" @click="gotoDriveDetails(drive)">View Details</button>
          </div>
          
        </div>
      </div>
    </div>
  </div>
</template>

