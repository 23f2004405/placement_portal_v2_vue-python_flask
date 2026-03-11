<script setup>
import {ref,onMounted,watch} from "vue"
import { useRoute,useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth"

const route = useRoute()
const authstore = useAuthStore()
const drive = ref({})
const error=ref(null)
const router = useRouter()
const closing = ref(false)
const loading = ref(null)

const fetchdrivedetail= async ()=>{
    error.value=false
    loading.value=true
try{
    const response = await fetch(`http://localhost:5000/api/company/drives/${route.params.drive_id}`,{
    headers:{
        "Authentication-Token": authstore.token
    }
    })
    const data = await response.json()
    if (!response.ok) {
      throw new Error(data.message||"Failed to fetch drive")
    }
    drive.value=data
}
catch(err){
    error.value=err.message
}finally{
  loading.value=false
}
}
const closeDrive = async () => {
  try {
    closing.value = true
    error.value=false

    const response = await fetch(`http://localhost:5000/api/company/drives/${drive.value.id}/close`, {
      method: "PUT",
      headers: {
        "Authentication-Token": authstore.token
      }
    })

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.message || "Failed to close drive")
    }

    drive.value.status = "CLOSED"

  } catch (err) {
    error.value = err.message
  } finally {
    closing.value = false
  }
}

const goToApplications = () => {
  router.push(`/company/drives/${drive.value.id}/applications`)
}
onMounted(()=>{
    fetchdrivedetail()
})

</script>

<template>
  <div class="container mt-4">

    <div v-if="error" class="alert alert-danger">
      {{ error }}
    </div>

    <div v-else-if="loading" class="text-center">
      <p>Loading drive details...</p>
    </div>

    <div v-else class="card shadow-sm p-4">

      <div class="d-flex justify-content-between align-items-center mb-3">
        <h3 class="mb-0">{{ drive.title }}</h3>

        <span>
          {{ drive.status }}
        </span>
      </div>

      <hr />

      <p><strong>Description:</strong></p>
      <p>{{ drive.description || 'No description provided.' }}</p>

      <div class="row mt-3">
        <div class="col-md-6">
          <p><strong>Minimum CGPA:</strong> {{ drive.min_cgpa ?? 'Not specified' }}</p>
        </div>
        <div class="col-md-6">
          <p>
            <strong>Application Deadline:</strong>
            {{ new Date(drive.deadline).toLocaleString() ?? 'Not specified' }}
          </p>
        </div>
        <div class="col-md-6">
          <p>
            <strong>Application Count:</strong>
            {{ drive.application_count}}
          </p>
        </div>
      </div>

      <div class="mt-4 d-flex gap-2">

        <button v-if="drive.status !== 'CLOSED'" class="btn btn-danger" :disabled="closing" @click="closeDrive">{{ closing ? "Closing drive" : "Close Drive" }}</button>

        <button class="btn btn-primary" @click="goToApplications">View Applications</button>

      </div>

    </div>
  </div>
</template>