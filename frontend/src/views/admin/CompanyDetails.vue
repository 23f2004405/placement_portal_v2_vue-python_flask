<script setup>
import {ref,onMounted} from "vue"
import { useRoute } from "vue-router";
import { useAuthStore } from "@/stores/auth";

const error=ref(null)
const loading=ref(null)
const action_error=ref(null)
const action_success=ref(null)
const authstore =  useAuthStore()
const route = useRoute()
const company = ref(null)

const fetchCompany = async ()=>{
    error.value=null
    loading.value=true
    try{
        const response = await fetch(`http://127.0.0.1:5000/api/admin/company/${route.params.company_id}`,{
            headers:{
                "Authentication-Token":authstore.token
            }
        })
        const data = await response.json()
        if (!response.ok){
            throw new Error(data.message||"Could not fetch Company Details.")
        }
        company.value=data
    }catch(err){
        error.value=err.message
    }finally{
        loading.value=false
    }
}
onMounted(()=>{
    fetchCompany()
})

const toggleBlacklist = async ()=>{
    action_error.value=null
    action_success.value=null
    try{
        const response = await fetch(`http://127.0.0.1:5000/api/admin/company/blacklist/${company.value.company_id}`,{
            method:'PUT',
            headers:{
                'Authentication-Token':authstore.token,
                "Content-Type":"application/json"
            },
            body:JSON.stringify({"role":"COMPANY"})
        })
        const data = await response.json()
        if (!response.ok){
            throw new Error(data.message||"Action Failed.")
        }
        company.value.is_blacklisted=data.is_blacklisted
        action_success.value=data.message
    }catch(err){
        action_error.value=err.message
    }
}

const changeApprovalStatus = async (status) => {
    action_error.value = null
    action_success.value = null

    try{
        const response = await fetch(`http://127.0.0.1:5000/api/admin/company/approval/${company.value.company_id}`,{
            method:'PUT',
            headers:{
                'Authentication-Token':authstore.token,
                "Content-Type":"application/json"
            },
            body:JSON.stringify({
                new_status: status
            })
        })

        const data = await response.json()

        if(!response.ok){
            throw new Error(data.message || "Action Failed.")
        }

        company.value.approval_status = data.approval_status
        action_success.value = data.message

    }catch(err){
        action_error.value = err.message
    }
}
</script>

<template>
<div class="container mt-4">
    <div v-if="loading">Loading...</div>
    <div v-if="error" class="alert alert-danger">{{ error }}</div>
    <div v-if="company">
        <h3 class="mb-3">Company Details</h3>
        <ul class="list-group mb-3">
            <li class="list-group-item"><strong>Company Id:</strong> {{ company.company_id }}</li>
            <li class="list-group-item"><strong>Name:</strong> {{ company.company_name }}</li>
            <li class="list-group-item"><strong>HR Contact:</strong> {{ company.hr_contact }}</li>
            <li class="list-group-item"><strong>Website:</strong> {{ company.website }}</li>
            <li class="list-group-item"><strong>Username:</strong> {{ company.username }}</li>
            <li class="list-group-item"><strong>Email:</strong> {{ company.email }}</li>
            <li class="list-group-item"><strong>Approval Status:</strong> {{ company.approval_status }}</li>
            <li class="list-group-item">
                <strong>Status:</strong>
                <span v-if="company.is_blacklisted === false" class="text-success">Active</span>
                <span v-else class="text-danger">Blacklisted</span>
            </li>
        </ul>
       
        
        <div class="mt-2">
        <button v-if="company.is_blacklisted" @click="toggleBlacklist" class="btn btn-danger"> Remove Blacklist</button>
        <button v-else @click="toggleBlacklist" class="btn btn-success"> Blacklist</button>

        <button v-if="company.approval_status === 'PENDING' || company.approval_status === 'REJECTED'" @click="changeApprovalStatus('approve')" class="btn btn-primary me-2">Approve Company</button>

        <button v-if="company.approval_status === 'PENDING'" @click="changeApprovalStatus('reject')" class="btn btn-warning">Reject Company</button>

        </div>
         
        <div v-if="action_success" class="alert alert-success mt-3">
          {{ action_success }}
        </div>

        <div v-if="action_error" class="alert alert-danger mt-3">
          {{ action_error }}
        </div>
    </div>
</div>
</template>