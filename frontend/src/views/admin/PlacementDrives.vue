<script setup>
import {ref,onMounted} from "vue"
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const drives= ref([])
const router = useRouter()
const authstore = useAuthStore()
const loading = ref(null)
const error = ref(null)
const filters = ref({
  company_name: "",
  company_username: "",
  drive_id: null,
  status:null
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

const fetchDrives = async ()=> {
  loading.value = true
  error.value = null
  try{
  const query =buildQueryParams()
  const response = await fetch(`http://localhost:5000/api/admin/drives?${query}`,{
    headers:{
      "Authentication-Token":authstore.token,
    }
  })
  const data = await response.json()
  if (!response.ok){
    throw new Error(data.message||'Could not fetch drives.')
  }
  drives.value= data
}catch(err){
  error.value=err.message
} finally {
  loading.value=false
}
}
const resetFilters = async ()=>{
filters.value = {

    company_name: "",
    company_username: "",
    drive_id: null,
    status: null
  }
  await fetchDrives()
}
const gotoDriveDetails =(drive)=>{
  router.push(`/admin/drive/${drive.drive_id}`)
}
onMounted(() => {
  fetchDrives()
})

</script>

<template>
<div class="container mt-4">
    <h2 class="mb-4">Drives</h2>
  <div class="row mb-3">
        <div class="col-md-3">
          <label class="form-label">Company Name</label>
          <input
            v-model="filters.company_name"
            type="text"
            class="form-control"
          />
        </div>

        <div class="col-md-3">
          <label class="form-label">Company Username</label>
          <input
            v-model="filters.company_username"
            type="text"
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

      <div class="col-md-3">
          <label class="form-label">Company Name</label>
          <input
            v-model="filters.company_name"
            type="text"
            class="form-control"
          />
      </div>

      <div class="col-md-3">
          <label CLASS="form-label">Status</label>
          <select v-model="filters.status" class="form-select" >
              <option :value="null">All</option>
              <option value="PENDING">PENDING</option>
              <option value="APPROVED">APPROVED</option>
              <option value="CLOSED">CLOSED</option>
              <option value="CANCELLED">CANCELLED</option>
            </select>
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
      <div class="col-md-4 mb-3" v-for="drive in drives" :key="drive.drive_id">
        <div class="card h-100">
          <div class="card-body">
            <h5 class="card-title">{{drive.title}}</h5>
            <p class="card-text">
              <strong>Drive ID:</strong> {{ drive.drive_id}} <br />
              <strong>Company Name:</strong> {{ drive.company_name }} <br />
              <strong>Company Username :</strong> {{ drive.company_username }} <br />
            </p>
            <button class="btn btn-primary" @click="gotoDriveDetails(drive)">View Details</button>
          </div>
          
        </div>
      </div>
    </div>
  
</template>