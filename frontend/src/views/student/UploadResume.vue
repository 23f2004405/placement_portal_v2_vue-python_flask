<template>
  <div class="container mt-5">
    <div class="card shadow p-4">

      <h3 class="mb-4">Upload Resume</h3>

      <div v-if="successMessage" class="alert alert-success">
        {{ successMessage }}
      </div>

      <div v-if="errorMessage" class="alert alert-danger">
        {{ errorMessage }}
      </div>

      <form @submit.prevent="uploadResume">

        <div class="mb-3">
          <label class="form-label">Select Resume (PDF only)</label>
          <input type="file" accept=".pdf" @change="handleFileChange"  class="form-control"/>
        </div>

        <button type="submit" :disabled="loading" class="btn btn-primary">
          <span v-if="loading">Uploading...</span>
          <span v-else>Upload Resume</span>
        </button>

      </form>

    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { useAuthStore } from "@/stores/auth"

const selectedFile = ref(null)
const loading = ref(false)
const errorMessage = ref(null)
const successMessage = ref(null)
const authstore = useAuthStore()

const handleFileChange = (event) => {

  errorMessage.value = false
  successMessage.value = false

  const file = event.target.files[0]

  if (!file) return

  if (!file.name.toLowerCase().endsWith(".pdf")) {
    errorMessage.value = "Only PDF files are allowed"
    return
  }

  selectedFile.value = file
}

const uploadResume = async () => {

  if (!selectedFile.value) {
    errorMessage.value = "Please select a resume first"
    return
  }

  loading.value = true
  errorMessage.value = false
  successMessage.value = false

  try {

    const formData = new FormData()

    // name must match request.files["resume"] in Flask
    formData.append("resume", selectedFile.value)

    const response = await fetch("http://localhost:5000/api/student/upload_resume", {
      method: "POST",
      body: formData,
      headers: {
        'Authentication-Token':authstore.token
      }
    })

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.message)
    }

    successMessage.value = data.message

  } catch (error) {
    errorMessage.value = error.message
  }

  loading.value = false
}
</script>