<script setup>
import {ref,onMounted} from "vue"
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const students= ref([])
const router = useRouter()
const authstore = useAuthStore()
const loading = ref(null)
const error = ref(null)
const filters = ref({
  name: "",
  username: "",
  student_id: null
})

const buildQueryParams = () =>{
  const params = new URLSearchParams()

  Object.entries(filters.value).forEach(([key,value])=>{
    if (typeof value === "string") {
      value = value.trim()
    }
    if (value != null && value != "" && value != undefined){
        params.append(key,value)
    }
  })
  return params.toString()
}

const fetchStudents = async ()=> {
  error.value=null
  loading.value=true
  try{
  const query =buildQueryParams()
  const response = await fetch(`http://localhost:5000/api/admin/students?${query}`,{
    headers:{
      "Authentication-Token":authstore.token,
    }
  })
  const data = await response.json()
  if (!response.ok){
    throw new Error(data.message||'Could not fetch students.')
  }
  students.value= data
}catch(err){
  error.value=err.message
} finally {
  loading.value=false
}
}
const resetFilters = async ()=>{
filters.value = {

    name: "",
    username: "",
    student_id: null
  }
  await fetchStudents()
}
const gotoStudentDetails =(student)=>{
  router.push(`/admin/student/${student.student_id}`)
}
onMounted(() => {
  fetchStudents()
})

</script>

<template>
<div class="container mt-4">
    <h2 class="mb-4">Students</h2>

        <div class="col-md-3">
          <label class="form-label">Name</label>
          <input
            v-model="filters.name"
            type="text"
            class="form-control"
          />
        </div>

        <div class="col-md-3">
          <label class="form-label">Username</label>
          <input
            v-model="filters.username"
            type="text"
            class="form-control"
          />
        </div>

        <div class="col-md-3">
          <label class="form-label">Student ID</label>
          <input
            v-model.number="filters.student_id"
            type="number"
            class="form-control"
          />
        </div>
      </div>

      <div class="mt-3">
        <button class="btn btn-primary me-2" @click="fetchStudents">
          Search
        </button>
        <button class="btn btn-secondary" @click="resetFilters">
          Reset
        </button>
      </div>
   

   
    <div v-if="loading" class="text-center">
      <div class="spinner-border">Loading...</div>
    </div>

    
    <div v-if="error" class="alert alert-danger">
      {{ error }}
    </div>

    <div v-if="!loading && students.length === 0" class="text-muted">
      No stuents found.
    </div>

    <div class="row">
      <div class="col-md-4 mb-3" v-for="student in students" :key="student.student_id">
        <div class="card h-100">
          <div class="card-body">
            <h5 class="card-title">{{student.name}}</h5>
            <p class="card-text">
              
              <strong>Student ID:</strong> {{ student.student_id }} <br />
              <strong>Username :</strong> {{ student.username }} <br />
            </p>
            <button class="btn btn-primary" @click="gotoStudentDetails(student)">View Details</button>
          </div>
          
        </div>
      </div>
    </div>
  
</template>