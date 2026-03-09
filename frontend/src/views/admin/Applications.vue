<script setup>
import {ref,onMounted} from "vue"
import { useRoute } from "vue-router"
import { useAuthStore } from "@/stores/auth"

const route = useRoute()
const authstore = useAuthStore()
const applications = ref([])
const error = ref(null)
const loading = ref(null)

const fetchapplications = async () => {
    error.value=null
    loading.value=true
    try{
        const response = await fetch(`http://localhost:5000/api/admin/drive/${route.params.drive_id}/applications`,{
            headers:{
                "Authentication-Token":authstore.token
            }
        })
        const data = await response.json()
        if (!response.ok){
            throw new Error(data.message||"The drives could not be fetched.")
        }
        applications.value=data
    }
    catch(err){
        error.value=err.message
    }finally{
      loading.value=false
    }
}
onMounted(()=>{
    fetchapplications()
})


</script>

<template>
 <div class="container mt-4">

    <div v-if="error" class="alert alert-danger">
      {{ error }}
    </div>

    <div v-else-if="loading" class="text-center">
      <p>Loading applications</p>
    </div>
    <div v-else-if="!loading && applications.length === 0" class="text-muted">
      No applications yet.
    </div>
    
    <div class="row">
      <div class="col-md-6 col-lg-4 mb-4" v-for="application in applications" :key="application.application_id">
        <div class="card h-100 shadow-sm">
          <div class="card-body">
            <h4 class="card-title">{{ application.student_name }}</h4>
            <p>Application ID:{{ application.application_id }}</p>
            <h5>Roll Number:{{application.roll_number }}</h5>
            <h5>Student ID:{{ application.student_id }}</h5>
            <ul class="list-group list-group-flush mb-3">
              <li class="list-group-item">
                <strong>Status:</strong>
                <span class="badge bg-secondary text-capitalize">
                  {{ application.status }}
                </span>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
</div>
 
</template>