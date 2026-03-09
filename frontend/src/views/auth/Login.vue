<script setup>
import {ref} from "vue"
import { useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth"

const username = ref(null)
const password = ref(null)
const error = ref(null)
const loading =ref(false)

const router = useRouter()
const authstore = useAuthStore()

async function handleLogin() {
  error.value=null
  loading.value=true

  try{
    const response = await fetch("http://localhost:5000/api/login",{
      method:"POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        username: username.value,
        password: password.value
      })
    })
      const data = await response.json()
      if (!response.ok) {
      throw new Error(data.message || "Login failed")
    }
    authstore.login(data.user_details)
     if (authstore.role === "ADMIN") {
      router.push("/admin/dashboard")
    } else if (authstore.role === "STUDENT") {
      router.push(`/student/${authstore.role_based_id}`)
    } else if (authstore.role === "COMPANY") {
      router.push(`/company/${authstore.role_based_id}`)
    }
    }
    catch (err) {
    error.value = err.message
  } finally {
    loading.value = false
  }
}

  

</script>

<template>
  <div class="container d-flex justify-content-center align-items-center vh-100">
    <div class="card shadow p-4" style="width: 400px;">
      <h3 class="text-center mb-4">Login</h3>

      <form @submit.prevent="handleLogin">
        
        <div class="mb-3">
          <label class="form-label">Username</label>
          <input 
            v-model="username"
            type="text"
            class="form-control"
            required
          />
        </div>

        <div class="mb-3">
          <label class="form-label">Password</label>
          <input 
            v-model="password"
            type="password"
            class="form-control"
            required
          />
        </div>

        <button 
          type="submit" 
          class="btn btn-primary w-100"
          :disabled="loading"
        >
          {{ loading ? "Logging in..." : "Login" }}
        </button>

        <div v-if="error" class="alert alert-danger mt-3">
          {{ error }}
        </div>

      </form>
    </div>
  </div>
</template>