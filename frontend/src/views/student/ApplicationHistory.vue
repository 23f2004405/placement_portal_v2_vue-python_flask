<script setup>
import {ref,onMounted,watch} from "vue"
import { useRouter, useRoute } from "vue-router"
import { useAuthStore } from "@/stores/auth";


const router = useRouter()
const authstore = useAuthStore()
const error = ref(null)
const loading = ref(null)
const applications = ref([])
const route = useRoute()

const fetchapplications = async ()=> {
    loading.value=true
    error.value=null

    const status = route.query.status
    try{
        const response = await fetch(`http://localhost:5000/api/student/applications?application_status=${status}`,{
            headers:{
                'Authentication-Token':authstore.token
            }
        })
        const data = await response.json()
        if (!response.ok){
            throw new Error(data.message||"The Applications could not be fetched.")
        }
        applications.value=data
    }catch(err){
        error.value=err.message
    }finally{
        loading.value=false
    }
}
onMounted(()=>{
    fetchapplications()
})

const gotoDriveDetails =(application)=>{
  router.push(`/student/drive/${application.drive_id}`)
}

watch(
  () => route.query.status,
  () => {
    fetchapplications()
  }
)
</script>

<template>
<div v-if="error" class="alert alert-danger">
      {{ error }}
    </div>
    <div v-else-if="loading">
        Loading Applications
    </div>

    <div v-else-if="!loading && applications.length === 0" class="text-muted">
      No Applications found.
    </div>

    <div class="row">
      <div
        class="col-md-4 mb-3"
        v-for="application in applications"
        :key="application.application_id"
      >
        <div class="card h-100">
          <div class="card-body">
            <h5 class="card-title">{{ application.title }}</h5>
            <p class="card-text">
              <strong>Application ID:</strong>{{ application.application_id }} <br />
              <strong>Company:</strong> {{ application.company_name }} <br />
              <strong>Drive ID:</strong> {{ application.drive_id }} <br />
              <strong>Status:</strong> {{ application.status }}
            </p>
            <button class="btn btn-primary" @click="gotoDriveDetails(application)">View Details</button>
          </div>
          
        </div>
      </div>
    </div>
  
</template>