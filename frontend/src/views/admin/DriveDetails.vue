<script setup>
import {ref,onMounted} from "vue"
import { useRoute,useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth"

const route = useRoute()
const authstore = useAuthStore()
const drive = ref(null)
const error=ref(null)
const router = useRouter()
const loading = ref(null)

const fetchdrivedetail= async ()=>{
    error.value=null
    loading.value=true
try{
    const response = await fetch(`http://localhost:5000/api/admin/drive/${route.params.drive_id}`,{
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


const goToApplications = () => {
  router.push(`/admin/drive/${drive.value.id}/applications`)
}
onMounted(()=>{
    fetchdrivedetail()
})

const updateDriveStatus = async (action) => {
  try {
    loading.value = true
    error.value = null

    const response = await fetch(
      `http://localhost:5000/api/admin/drive/${route.params.drive_id}/approval`,
      {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": authstore.token
        },
        body: JSON.stringify({ "action":action })
      }
    )

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.message || "Action failed")
    }

    if (action === "approve") {
      drive.value.status = "APPROVED"
    }

    if (action === "reject") {
      drive.value.status = "REJECTED"
    }

  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

</script>

<template>
  <div class="container mt-4">

    <div v-if="error" class="alert alert-danger">
      {{ error }}
    </div>

    <div v-else-if="loading" class="text-center">
      <p>Loading drive details...</p>
    </div>

    <div v-else-if="drive" class="card shadow-sm p-4">

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
            {{new Date(drive.deadline).toLocaleString() ?? 'Not specified' }}
          </p>
        </div>
      </div>
        <div class="mt-4 d-flex gap-2">

  <button class="btn btn-primary" @click="goToApplications">
    View Applications
  </button>

  <button
    v-if="drive.status === 'PENDING'"
    class="btn btn-success"
    @click="updateDriveStatus('approve')"
  >
    Approve Drive
  </button>

  <button
    v-if="drive.status === 'PENDING'"
    class="btn btn-danger"
    @click="updateDriveStatus('reject')"
  >
    Reject Drive
  </button>

</div>

      

        


     

    </div>
  </div>
</template>