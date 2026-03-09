<script setup>
import {ref,onMounted} from "vue"
import { useAuthStore } from "@/stores/auth"

const authstore = useAuthStore()
const error = ref(null)
const student = ref(null)
const loading = ref(false)
const fetchstudent =  async () =>{
    error.value=null
    loading.value=true
    try{
        const response = await fetch(`http://localhost:5000/api/student/${authstore.role_based_id}`,{
            headers:{
                'Authentication-Token':authstore.token
            }
        })
        const data = await response.json()
        if (!response.ok){
            throw new Error(data.message||"Try again later.")
        }
        student.value= data
    }catch(err){
        error.value=err.message
    }finally{
      loading.value=false
    }
}
onMounted(()=>{
  fetchstudent()
})

</script>

<template>
<div class="container mt-5">

    <div class="card shadow">
      <div class="card-header bg-dark text-white">
        Student Profile
      </div>

      <div class="card-body">

        <div v-if="loading" class="text-center">
          Loading...
        </div>

        <div v-else-if="error" class="alert alert-danger">
          {{ error }}
        </div>

        <div v-else-if="student">

          <div class="row mb-3">
            <div class="col-md-6">
              <strong>Username:</strong>
              <p>{{ student.username }}</p>
            </div>

            <div class="col-md-6">
              <strong>Name:</strong>
              <p>{{student.name}}</p>
            </div>
          </div>

          <div class="row mb-3">
            <div class="col-md-6">
              <strong>Roll Number:</strong>
              <p>{{student.roll_number}}</p>
            </div>

            <div class="col-md-6">
              <strong>CGPA:</strong>
              <p>{{student.cgpa ?? "NA"}}</p>
            </div>
          </div>

          <div class="row mb-3">
            <div class="col-md-6">
              <strong>Email:</strong>
              <p>{{ student.email ?? "NA" }}</p>
            </div>
          </div>

          <div class="row mb-3">
            <div class="col-md-6">
              <strong>Department:</strong>
              <p>{{ student.department ?? "NA"}}</p>
            </div>
          </div>

          <div class="row mb-3">
            <div class="col-md-6">
              <strong>Passing out year:</strong>
              <p>{{ student.passing_out_year ?? "NA"}}</p>
            </div>
          </div>
          
          <div class="col-md-6">
          <p>
          <strong>Resume:</strong>
          <a  v-if="student.resume" :href="`http://localhost:5000/api/resume/${student.resume}`" target="_blank" class="btn btn-outline-primary btn-sm">View Resume</a>
          <span v-else class="text-muted">Not uploaded</span>
        </p>
        </div>
          

        </div>

      </div>
    </div>

  </div>
</template>