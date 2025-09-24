<template>
  <div class="page-container">
    <header v-if="showNav">
      <nav class="navbar">
        <NuxtLink to="/" class="nav-link">Home</NuxtLink>
        <NuxtLink to="/report" class="nav-link">Report</NuxtLink>
        <NuxtLink to="/search" class="nav-link">Search</NuxtLink>
        <NuxtLink to="/gallery" class="nav-link">Gallery</NuxtLink>
        <NuxtLink to="/contact" class="nav-link">Contact</NuxtLink>
        <NuxtLink to="/chatbot" class="nav-link">Chatbot</NuxtLink>
      </nav>
    </header>

    <main>
      <NuxtPage />
    </main>

    <footer class="footer">
      <p>© 2025 Family Reunion. All rights reserved.</p>
    </footer>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'

const route = useRoute()

const showNav = computed(() => {
  return route.path !== '/login'
})
</script>

<style scoped>
.page-container {
  background: url("/images/family-hugging.jpg") no-repeat center center/cover;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  animation: fadeIn 2s ease-in-out;
}

.navbar {
  display: flex;
  justify-content: center;
  gap: 2rem;
  padding: 1rem;
  background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
  color: white;
  animation: slideDown 1s ease-in-out;
  position: sticky;
  top: 0;
  z-index: 1000;
  border-bottom: 2px solid #ffc107;
}

.nav-link {
  color: #fff;
  font-weight: bold;
  text-decoration: none;
  transition: color 0.3s ease, transform 0.3s ease;
}

.nav-link:hover {
  color: #ffc107;
  transform: scale(1.1);
}

.footer {
  text-align: center;
  background: #2c5364;
  color: white;
  padding: 1rem;
  font-size: 0.9rem;
  animation: fadeIn 1.5s ease-in;
  border-top: 2px solid #ffc107;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes slideDown {
  from { transform: translateY(-100%); }
  to { transform: translateY(0); }
}
</style>
