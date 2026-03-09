import { defineStore } from "pinia"
import { ref, computed } from "vue"

export const useAuthStore = defineStore("auth", () => {

  const token = ref(localStorage.getItem("token") || null)
  const role = ref(localStorage.getItem("role") || null)
  const username = ref(localStorage.getItem("username") || null)
  const role_based_id = ref(localStorage.getItem("role_based_id")|| null)

  const isAuthenticated = computed(() => !!token.value)

  function login(userDetails) {
    token.value = userDetails.auth_token
    role.value = userDetails.roles[0]
    username.value = userDetails.username
    role_based_id.value = userDetails.role_based_id

    localStorage.setItem("token", token.value)
    localStorage.setItem("role", role.value)
    localStorage.setItem("username", username.value)
    localStorage.setItem("role_based_id",role_based_id.value)
  }

  async function logout() {
    try {
      if (token.value) {
        await fetch("http://localhost:5000/api/logout", {
          method: "POST",
          headers: {
            "Authentication-Token": token.value
          }
        })
      }
    } catch (err) {
      console.error("Logout API failed:", err)
    }

    token.value = null
    role.value = null
    username.value = null
    role_based_id.value = null

    localStorage.removeItem("token")
    localStorage.removeItem("role")
    localStorage.removeItem("username")
    localStorage.removeItem("role_based_id")
  }

  return {
    token,
    role,
    username,
    role_based_id,
    isAuthenticated,
    login,
    logout
  }
})