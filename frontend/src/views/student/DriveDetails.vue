<script setup>
import { ref, onMounted } from "vue"
import { useRoute } from "vue-router"
import { useAuthStore } from "@/stores/auth"

const drive = ref(null)
const error = ref(null)
const loading = ref(false)
const can_apply = ref(false)
const apply_error = ref(null)
const apply_success = ref(null)
const route = useRoute()
const authstore = useAuthStore()

const fetchdrive = async () => {
  error.value = null
  loading.value = true

  try {
    const response = await fetch(
      `http://localhost:5000/api/student/drive/${route.params.drive_id}`,
      {
        headers: {
          "Authentication-Token": authstore.token
        }
      }
    )

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.message || "Details could not be fetched.")
    }

    drive.value = data
    can_apply.value = data.can_apply

  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchdrive()
})

const applydrive = async () => {
  apply_error.value = null
  apply_success.value = null

  try {
    const response = await fetch(
      `http://localhost:5000/api/student/drive/${route.params.drive_id}/apply`,
      {
        method: "POST",
        headers: {
          "Authentication-Token": authstore.token
        }
      }
    )

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.message || "Action Failed.")
    }

    apply_success.value = data.message
    can_apply.value = false

  } catch (err) {
    apply_error.value = err.message
  }
}
</script>

<template>
<div class="container mt-4">

  <div v-if="apply_error" class="alert alert-danger">
    {{ apply_error }}
  </div>

  <div v-if="apply_success" class="alert alert-success">
    {{ apply_success }}
  </div>

  <div v-if="error" class="alert alert-danger">
    {{ error }}
  </div>

  <div v-else-if="loading" class="text-center">
    <p>Loading drive details...</p>
  </div>

  <div v-else-if="drive" class="card shadow-sm p-4">

    <div class="d-flex justify-content-between align-items-center mb-3">
      <h3 class="mb-0">{{ drive.title }}</h3>
      <p><strong>Company Id:</strong> {{ drive.company_id }}</p>
      <p><strong>Company Name:</strong> {{ drive.company_name }}</p>
    </div>

    <hr />

    <p><strong>Description:</strong></p>
    <p>{{ drive.description || "No description provided." }}</p>

    <div class="row mt-3">

      <div class="col-md-6">
        <p><strong>Minimum CGPA:</strong> {{ drive.min_cgpa ?? "Not specified" }}</p>
      </div>

      <div class="col-md-6">
        <p><strong>Passing Out Year:</strong> {{ drive.passing_out_year ?? "Not specified" }}</p>
      </div>

      <div class="col-md-6">
        <p><strong>Website:</strong> {{ drive.website ?? "Not specified" }}</p>
      </div>

      <div class="col-md-6">
        <p><strong>HR Contact:</strong> {{ drive.hr_contact ?? "Not specified" }}</p>
      </div>

      <div class="col-md-6">
        <p>
          <strong>Application Deadline:</strong>
          {{ new Date(drive.application_deadline).toLocaleDateString() ?? "Not specified" }}
        </p>
      </div>

    </div>

  </div>

  <div v-if="drive" class="mt-4 d-flex gap-2">
    <button v-if="can_apply" class="btn btn-primary" :disabled="!can_apply" @click="applydrive">Apply</button>
  </div>

</div>
</template>