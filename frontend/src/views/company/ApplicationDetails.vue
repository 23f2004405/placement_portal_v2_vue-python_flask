<script setup>
import {ref,onMounted} from "vue"
import { useRoute } from "vue-router"
import { useAuthStore } from "@/stores/auth"

const route = useRoute()
const authstore = useAuthStore()
const application= ref(null)
const error = ref(null)
const loading = ref(null)


const fetchapplicationdetail = async () => {
    error.value=false
    loading.value=true
    try{
        const response = await fetch(`http://localhost:5000/api/company/application/${route.params.application_id}`,{
            headers:{
                "Authentication-Token": authstore.token
            }
        })
        const data = await response.json()
        if (!response.ok){
            throw new Error(data.message||'Application could not be fetched.')
        }
        application.value=data
    }catch(err){
        error.value= err.message
    }finally{
      loading.value=false
    }
  }
onMounted(()=>{
    fetchapplicationdetail()
})
const changeApplicationStatus= async (newstatus) => {
    error.value=false
    try{
        const response = await fetch(`http://localhost:5000/api/company/application/change_status/${route.params.application_id}`,{
          method:'PUT',  
          headers:{
                'Authentication-Token':authstore.token,
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                status:newstatus
            })})
        const data = await response.json()
        if (!response.ok){
            throw new Error(data.message||'Action failed.')
        }
        application.value.status=newstatus
    }catch(err){
        error.value=err.message
    }

}
</script>

<template>
<div class="container mt-4">

    <div v-if="error" class="alert alert-danger">
      {{ error }}
    </div>

    <div v-else-if="loading" class="text-center">
      <p>Loading Application details...</p>
    </div>
<div v-else-if="application" class="card shadow-sm p-4">

      <div class="d-flex justify-content-between align-items-center mb-3">
        <h3 class="mb-0">{{ application.application_id }}</h3>

         <span 
        class="badge"
        :class="{
          'bg-secondary': application.status === 'APPLIED',
          'bg-warning text-dark': application.status === 'SHORTLISTED',
          'bg-success': application.status === 'SELECTED',
          'bg-danger': application.status === 'REJECTED'
        }"
      >
        {{ application.status }}
      </span>
      </div>

      <hr />


      <div class="row mt-3">
        <div class="col-md-6">
          <p><strong>Name:</strong> {{ application.student_details.name}}</p>
        </div>
        <div class="col-md-6">
          <p>
            <strong>Roll Number:</strong>
            {{ application.student_details.roll_number ?? 'Not specified' }}
          </p>
        </div>
         <div class="col-md-6">
          <p>
            <strong>Department:</strong>
            {{ application.student_details.department ?? 'Not specified' }}
          </p>
        </div>
         <div class="col-md-6">
          <p>
            <strong>CGPA:</strong>
            {{ application.student_details.cgpa ?? 'Not specified' }}
          </p>
        </div>
    
       <div class="col-md-6">
          <p>
          <strong>Resume:</strong>
          <a  v-if="application.student_details.resume" :href="`http://localhost:5000/api/resume/${application.student_details.resume}`" target="_blank" class="btn btn-outline-primary btn-sm">View Resume</a>
          <span v-else class="text-muted">Not uploaded</span>
        </p>
        </div>
        
      </div>

      <div class="mt-4 d-flex gap-2 flex-wrap">

     
      <template v-if="application.status === 'APPLIED'">
        <button
          class="btn btn-warning"
          @click="changeApplicationStatus('SHORTLISTED')"
        >
          Shortlist
        </button>

        <button
          class="btn btn-danger"
          @click="changeApplicationStatus('REJECTED')"
        >
          Reject
        </button>
      </template>

     
      <template v-if="application.status === 'SHORTLISTED'">
        <button
          class="btn btn-success"
          @click="changeApplicationStatus('SELECTED')"
        >
          Select
        </button>

        <button
          class="btn btn-danger"
          @click="changeApplicationStatus('REJECTED')"
        >
          Reject
        </button>
      </template>

     
      <template v-if="application.status === 'SELECTED'">
        <span class="text-success fw-bold">
          Candidate Selected ✔
        </span>
      </template>

      <template v-if="application.status === 'REJECTED'">
        <span class="text-danger fw-bold">
          Candidate Rejected ✖
        </span>
      </template>

    </div>

    </div>
  </div>
</template>