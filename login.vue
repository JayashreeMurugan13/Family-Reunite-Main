<template>
  <div class="login-page">
    <div class="login-box">
      <h1>Volunteer Login</h1>
      <p class="subtext">Volunteers must log in to submit reports.</p>
      <input type="email" v-model="email" placeholder="Volunteer Email" />
      <input type="password" v-model="password" placeholder="Password" />
      <button @click="login">Login</button>
      <p v-if="error" class="error">{{ error }}</p>
      <div class="guest-access">
        <router-link to="/" class="guest-link">🔓 Continue as Public</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const email = ref('')
const password = ref('')
const error = ref('')
const router = useRouter()

const login = async () => {
  try {
    const response = await fetch('http://localhost:8000/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        username: email.value,
        password: password.value
      })
    })

    if (!response.ok) {
      const errorData = await response.json()
      throw new Error(errorData.detail || 'Login failed')
    }

    const data = await response.json()
    localStorage.setItem('auth_token', data.access_token)
    localStorage.setItem('user_email', email.value)
    router.push('/')
  } catch (err) {
    error.value = err.message
    console.error('Login error:', err)
  }
}
</script>

<style scoped>
.login-page {
  height: 100vh;
  background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.login-box {
  background: white;
  padding: 2.5rem;
  border-radius: 20px;
  box-shadow: 0 12px 35px rgba(0, 0, 0, 0.2);
  width: 320px;
  text-align: center;
  animation: slideIn 0.6s ease;
}

h1 {
  font-size: 24px;
  margin-bottom: 10px;
  color: #2c5364;
}

.subtext {
  font-size: 13px;
  margin-bottom: 20px;
  color: #555;
}

input {
  width: 100%;
  padding: 12px;
  margin: 10px 0;
  border: 1px solid #ccc;
  border-radius: 30px;
  font-size: 14px;
  transition: 0.3s ease;
}

input:focus {
  border-color: #2c5364;
  outline: none;
  box-shadow: 0 0 0 2px rgba(44, 83, 100, 0.2);
}

button {
  background: #2c5364;
  color: white;
  border: none;
  width: 100%;
  padding: 12px;
  border-radius: 30px;
  font-weight: bold;
  cursor: pointer;
  margin-top: 10px;
  transition: background 0.3s ease;
}

button:hover {
  background: #1f3547;
}

.error {
  color: #d9534f;
  font-size: 13px;
  margin-top: 10px;
}

.guest-access {
  margin-top: 20px;
  text-align: center;
  font-size: 13px;
}

.guest-link {
  text-decoration: none;
  color: #2c5364;
  font-weight: bold;
  transition: color 0.3s;
}

.guest-link:hover {
  color: #0f2027;
}

@keyframes slideIn {
  0% {
    opacity: 0;
    transform: translateY(20px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
