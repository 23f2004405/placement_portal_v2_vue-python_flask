<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"

const router = useRouter()

const form = ref({
  username: "",
  email: "",
  password: "",
  role: "STUDENT",
  name: "",
  roll_number: "",
  department: "",
  cgpa: "",
  passing_out_year: ""
})

const error = ref(null)
const success = ref(null)

const register = async () => {
  error.value = null
  success.value = null

  try {
    const response = await fetch("http://localhost:5000/api/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(form.value)
    })

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.message)
    }

    success.value = data.message

    setTimeout(() => {
      router.push("/login")
    }, 1500)

  } catch (err) {
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

            <h4 class="mb-4 text-center">Student Registration</h4>

            <div v-if="error" class="alert alert-danger">
              {{ error }}
            </div>

            <div v-if="success" class="alert alert-success">
              {{ success }}
            </div>

            <form @submit.prevent="register">

              <div class="mb-3">
                <label class="form-label">Username</label>
                <input v-model="form.username" type="text" class="form-control" required />
              </div>

              <div class="mb-3">
                <label class="form-label">Email</label>
                <input v-model="form.email" type="email" class="form-control" required />
              </div>

              <div class="mb-3">
                <label class="form-label">Password</label>
                <input v-model="form.password" type="password" class="form-control" required />
              </div>

              <div class="mb-3">
                <label class="form-label">Full Name</label>
                <input v-model="form.name" type="text" class="form-control" required />
              </div>

              <div class="mb-3">
                <label class="form-label">Roll Number</label>
                <input v-model="form.roll_number" type="text" class="form-control" required />
              </div>

              <div class="mb-3">
                <label class="form-label">Department</label>
                <input v-model="form.department" type="text" class="form-control" required/>
              </div>

              <div class="mb-3">
                <label class="form-label">CGPA</label>
                <input v-model="form.cgpa" type="number" step="0.01" class="form-control" required />
              </div>

              <div class="mb-3">
                <label class="form-label">Passing Out Year</label>
                <input v-model.number="form.passing_out_year" type="number" class="form-control" required />
              </div>

              <button type="submit" class="btn btn-primary w-100">
                Register
              </button>

            </form>

          </div>
        </div>

      </div>
    </div>
  </div>
</template>