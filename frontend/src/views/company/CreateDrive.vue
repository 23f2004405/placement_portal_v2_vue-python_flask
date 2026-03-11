<script setup>
import {ref} from "vue"
import { useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth"

const router = useRouter()
const authstore = useAuthStore()

const error = ref()
const success = ref()

const form = ref({
    title:"",
    description:"",
    min_cgpa:"",
    passing_out_year:"",
    application_deadline:""
})

const createDrive = async () =>{
  error.value=false

  try{

        // convert datetime-local (local time) → UTC ISO string
        const payload = {
            ...form.value,
            application_deadline: new Date(form.value.application_deadline).toISOString()
        }

        const response = await fetch(`http://localhost:5000/api/company/create_drive`,{
            method:'POST',
            headers:{
                'Authentication-Token':authstore.token,
                "Content-Type": "application/json"
            },
            body: JSON.stringify(payload)
        })

        const data = await response.json()

        if (!response.ok){
            throw new Error(data.message)
        }

        success.value = data.message

        setTimeout(() => {
          router.push(`/company/${authstore.role_based_id}`)
        }, 2000)

    }catch(err){
        error.value = err.message
    }
}
</script>

<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">

        <div class="card shadow">
          <div class="card-body">

            <h4 class="mb-4 text-center">Create New Placement Drive</h4>

            <div v-if="error" class="alert alert-danger">
              {{ error }}
            </div>

            <div v-if="success" class="alert alert-success">
              {{ success }}
            </div>


            <form @submit.prevent="createDrive">

              <div class="mb-3">
                <label class="form-label">Title</label>
                <input v-model="form.title" type="text" class="form-control" required />
              </div>

              <div class="mb-3">
                <label class="form-label">Description</label>
                <textarea v-model="form.description" class="form-control" rows="4" required></textarea>
              </div>

              <div class="mb-3">
                <label class="form-label">Minimum CGPA</label>
                <input v-model="form.min_cgpa" type="number" class="form-control" />
              </div>

              <div class="mb-3">
                <label class="form-label">Passing Out Year</label>
                <input v-model="form.passing_out_year" type="number" class="form-control" />
              </div>

              <div class="mb-3">
                <label class="form-label">Application Deadline</label>
                <input v-model="form.application_deadline" type="datetime-local" class="form-control" required />
              </div>

              <button type="submit" class="btn btn-success w-100">
                Create
              </button>

            </form>

          </div>
        </div>

      </div>
    </div>
  </div>
</template>