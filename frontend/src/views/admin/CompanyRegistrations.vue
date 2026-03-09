<script setup>
import {ref,onMounted} from "vue"
import { useAuthStore} from "@/stores/auth"

const error= ref(null)
const loading = ref(null)
const authstore = useAuthStore()
const registrations=ref([])
const action_error=ref(null)
const action_success=ref(null)

const fetchregistrations = async ()=> {
    error.value=null
    loading.value=true
    try{
        const response = await fetch('http://localhost:5000/api/admin/company/registrations',{
            headers:{
                'Authentication-Token':authstore.token
            }
        })
        const data = await response.json()
        if (!response.ok){
            throw new Error(data.message||'Cant fetch registrations')
        }
        registrations.value=data
    }catch(err){
        error.value=err.message
    } finally {
        loading.value=false
    }
}
onMounted(()=>{
    fetchregistrations()
})

const approval_action = async (registration)=>{
action_error.value=null
action_success.value=null
    try{
        const response = await fetch(`http://localhost:5000/api/admin/company/approval/${registration.company_id}`,{
            method:"PUT",
            headers:{
                "Authentication-Token":authstore.token,
                 "Content-Type": "application/json"
            },
            body:JSON.stringify({
                "new_status":"approve"
            })
        })
        const data=await response.json()
        if (!response.ok){
            throw new Error(data.message||"Action Failed.")
        }
        registrations.value = registrations.value.filter(
         company => company.company_id !== registration.company_id
        )
        action_success.value=data.message
        setTimeout(() => {
        action_success.value = null
        action_error.value = null
        }, 3000)
    }catch(err){
        action_error.value=err.message
    }
}

const rejection_action = async (registration)=>{
action_error.value=null
action_success.value=null
    try{
        const response = await fetch(`http://localhost:5000/api/admin/company/approval/${registration.company_id}`,{
            method:"PUT",
            headers:{
                "Authentication-Token":authstore.token,
                 "Content-Type": "application/json"
            },
            body:JSON.stringify({
                "new_status":"reject"
            })
        })
        const data=await response.json()
        if (!response.ok){
            throw new Error(data.message||"Action Failed.")
        }
        registrations.value=registrations.value.filter(
            company => registration.company_id !== company.company_id
        )
        action_success.value=data.message
        setTimeout(() => {
        action_success.value = null
        action_error.value = null
        }, 3000)
    }catch(err){
        action_error.value=err.message
    }
}
</script>

<template>
<div class="container mt-4">

<div class="position-fixed top-0 end-0 p-3" style="z-index:1050">
  

  <div v-if="action_success" class="alert alert-success shadow">
    {{ action_success }}
  </div>

  <div v-if="action_error" class="alert alert-danger shadow">
    {{ action_error }}
  </div>

</div>

    <div v-if="error" class="alert alert-danger">
      {{ error }}
    </div>

    <div v-else-if="loading" class="text-center">
      <p>Loading registrations...</p>
    </div>

     <div v-else-if="!loading && registrations.length === 0" class="text-muted">
        No company registrations
    </div>
        
    <div v-else class="row">
      <div
        class="col-md-6 col-lg-4 mb-4"
        v-for="registration in registrations"
        :key="registration.company_id"
      >
      <div class="card shadow-sm mb-3">
        <div class="card-body d-flex justify-content-between align-items-start">

        <div>
        <h5 class="card-title">{{ registration.company_name }}</h5>

        <div><strong>Username:</strong> {{ registration.username }}</div>
        <div><strong>Email:</strong> {{ registration.email }}</div>
        <div><strong>Website:</strong> 
            <a :href="registration.website" target="_blank">
            {{ registration.website }}
            </a>
        </div>
        <div><strong>ID:</strong> {{ registration.company_id}}</div>
    </div>

    <div>
      <button class="btn btn-success btn-sm me-2" @click="approval_action(registration)">
        Approve
      </button>
      <button class="btn btn-danger btn-sm" @click="rejection_action(registration)">
        Reject
      </button>
    </div>

    </div>
    </div>  
    </div>
    </div>
</div>
</template>