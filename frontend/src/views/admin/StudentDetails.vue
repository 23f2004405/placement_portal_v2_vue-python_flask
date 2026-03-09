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
const student = ref(null)

const fetchStudent = async ()=>{
    error.value=null
    loading.value=true
    try{
        const response = await fetch(`http://127.0.0.1:5000/api/admin/student/${route.params.student_id}`,{
            headers:{
                "Authentication-Token":authstore.token
            }
        })
        const data = await response.json()
        if (!response.ok){
            throw new Error(data.message||"Could not fetch Company Details.")
        }
        student.value=data
    }catch(err){
        error.value=err.message
    }finally{
        loading.value=false
    }
}
onMounted(()=>{
    fetchStudent()
})

const toggleBlacklist = async ()=>{
    action_error.value=null
    action_success.value=null
    try{
        const response = await fetch(`http://127.0.0.1:5000/api/admin/student/blacklist/${student.value.student_id}`,{
            method:'PUT',
            headers:{
                'Authentication-Token':authstore.token,
                "Content-Type":"application/json"
            },
            body:JSON.stringify({"role":"STUDENT"})
        })
        const data = await response.json()
        if (!response.ok){
            throw new Error(data.message||"Action Failed.")
        }
        student.value.is_blacklisted=data.is_blacklisted
        action_success.value=data.message
    }catch(err){
        action_error.value=err.message
    }
}
</script>

<template>
<div class="container mt-4">
    <div v-if="loading">Loading...</div>
    <div v-else-if="error" class="alert alert-danger">{{ error }}</div>
    <div v-else-if="student">
        <h3 class="mb-3">Student Details</h3>
        <ul class="list-group mb-3">
            <li class="list-group-item"><strong>Student Id:</strong> {{ student.student_id }}</li>
            <li class="list-group-item"><strong>Username:</strong> {{ student.username }}</li>
            <li class="list-group-item"><strong>Name:</strong> {{ student.name }}</li>
            <li class="list-group-item"><strong>Roll Number:</strong> {{student.roll_number }}</li>
            <li class="list-group-item"><strong>Department</strong> {{ student.department }}</li>
            <li class="list-group-item"><strong>Cgpa:</strong> {{ student.cgpa }}</li>
            <li class="list-group-item"><strong>Email:</strong> {{ student.email }}</li>
            <li class="list-group-item">
            <p>
            <strong>Resume:</strong>
            <a  v-if="student.resume" :href="`http://localhost:5000/api/resume/${student.resume}`" target="_blank" class="btn btn-outline-primary btn-sm">View Resume</a>
            <span v-else class="text-muted">Not uploaded</span>
            </p>
            </li>
            <li class="list-group-item">
                <strong>Status:</strong>
                <span v-if="student.is_blacklisted === false" class="text-success">Active</span>
                <span v-else class="text-danger">Blacklisted</span>
            </li>
        </ul>
        <button v-if="student.is_blacklisted" @click="toggleBlacklist" class="btn btn-danger"> Remove Blacklist</button>
        <button v-else @click="toggleBlacklist" class="btn btn-success"> Blacklist</button>
         
        <div v-if="action_success" class="alert alert-success mt-3">
          {{ action_success }}
        </div>

        <div v-if="action_error" class="alert alert-danger mt-3">
          {{ action_error }}
        </div>
    </div>
</div>
</template>