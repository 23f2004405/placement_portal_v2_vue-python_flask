<script setup>
import { ref, onMounted } from "vue"
import { useAuthStore } from "@/stores/auth"
import { useRouter } from "vue-router"

const router = useRouter()

const authstore = useAuthStore()

const form = ref({
  name: "",
  cgpa: "",
  department: "",
  roll_number:"",
  passing_out_year:"",
  email:""
})

const loading = ref(false)
const error = ref(null)
const success = ref(null)

const fetchProfile = async () => {
  loading.value = true
  try {
    const response = await fetch(
      `http://localhost:5000/api/student/${authstore.role_based_id}`,
      {
        headers: {
          "Authentication-Token": authstore.token
        }
      }
    )

    const data = await response.json()

    if (!response.ok) throw new Error(data.message)

    form.value.name=data.name
    form.value.cgpa=data.cgpa
    form.value.department=data.department
    form.value.roll_number=data.roll_number
    form.value.email=data.email

  } catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

onMounted(fetchProfile)

const updateProfile = async () => {
  error.value = null

  try {
    const response = await fetch(
      "http://localhost:5000/api/student/edit_profile",
      {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "Authentication-Token": authstore.token
        },
        body: JSON.stringify(form.value)
      }
    )

    const data = await response.json()

    if (!response.ok) throw new Error(data.message)

    success.value = data.message
    setTimeout(() => {
          router.push(`/student/${authstore.role_based_id}`)
        }, 2000);

  } catch (err) {
    error.value = err.message
  }
}
</script>

<template>
  <div class="container mt-4">

    <div v-if="error" class="alert alert-danger">
      {{ error }}
    </div>

    <div v-if="success" class="alert alert-success">
      {{ success }}
    </div>

    <form @submit.prevent="updateProfile">

      <div class="mb-3">
        <label>Name</label>
        <input v-model="form.name" class="form-control" required>
      </div>

      <div class="mb-3">
        <label>CGPA</label>
        <input type="number" step="0.01" v-model.number="form.cgpa" class="form-control">
      </div>

      <div class="mb-3">
        <label>Department</label>
        <input v-model="form.department" class="form-control">
      </div>

      
      <div class="mb-3">
        <label>Roll Number</label>
        <input v-model="form.roll_number" class="form-control">
      </div>

      
      <div class="mb-3">
        <label>Passing Out Year</label>
        <input v-model.number="form.passing_out_year" type="number" class="form-control">
      </div>

      <div class="mb-3">
        <label>Email</label>
        <input v-model="form.email" type="email" class="form-control">
      </div>

      <button type="submit" class="btn btn-primary">
        Update Profile
      </button>

    </form>

  </div>
</template>