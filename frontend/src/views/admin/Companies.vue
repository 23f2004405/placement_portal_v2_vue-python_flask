<script setup>
import {ref,onMounted} from "vue"
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const companies= ref([])
const router = useRouter()
const authstore = useAuthStore()
const loading = ref(null)
const error = ref(null)
const filters = ref({
  company_name: "",
  username: "",
  company_id: null
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

const fetchCompanies = async ()=> {
  error.value=null
  loading.value=true
  try{
  const query =buildQueryParams()
  const response = await fetch(`http://localhost:5000/api/admin/companies?${query}`,{
    headers:{
      "Authentication-Token":authstore.token,
    }
  })
  const data = await response.json()
  if (!response.ok){
    throw new Error(data.message||'Could not fetch companies.')
  }
  companies.value= data
}catch(err){
  error.value=err.message
} finally {
  loading.value=false
}
}
const resetFilters = async ()=>{
filters.value = {

    company_name: "",
    username: "",
    company_id: null
  }
  await fetchCompanies()
}
const gotoCompanyDetails =(company)=>{
  router.push(`/admin/company/${company.company_id}`)
}
onMounted(() => {
  fetchCompanies()
})

</script>

<template>
<div class="container mt-4">
    <h2 class="mb-4">Companies</h2>

        <div class="col-md-3">
          <label class="form-label">Company Name</label>
          <input
            v-model="filters.company_name"
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
          <label class="form-label">Company ID</label>
          <input
            v-model.number="filters.company_id"
            type="number"
            class="form-control"
          />
        </div>
      </div>

      <div class="mt-3">
        <button class="btn btn-primary me-2" @click="fetchCompanies">
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

    <div v-if="!loading && companies.length === 0" class="text-muted">
      No companies found.
    </div>

    <div class="row">
      <div class="col-md-4 mb-3" v-for="company in companies" :key="company.company_id">
        <div class="card h-100">
          <div class="card-body">
            <h5 class="card-title">{{company.company_name}}</h5>
            <p class="card-text">
              <strong>Company ID:</strong> {{ company.company_id }} <br />
              <strong>Username :</strong> {{ company.username }} <br />
            </p>
            <button class="btn btn-primary" @click="gotoCompanyDetails(company)">View Details</button>
          </div>
          
        </div>
      </div>
    </div>
  
</template>