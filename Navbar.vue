<template>
  <nav class="flex justify-between p-4 bg-black bg-opacity-50">
    <h1 class="text-xl font-bold">Lost Finder</h1>
    <div class="space-x-4">
      <NuxtLink to="/">Home</NuxtLink>
      <NuxtLink to="/login">Login</NuxtLink>
      <NuxtLink to="/report">Report</NuxtLink>
      <NuxtLink to="/search">Search</NuxtLink>
      <NuxtLink to="/chatbot">Chatbot</NuxtLink>
      <NuxtLink to="/about">About</NuxtLink>
    </div>
  </nav>
</template>

<style scoped>
nav a {
  color: white;
  text-decoration: none;
  font-weight: 500;
}
nav a:hover {
  text-decoration: underline;
}
</style>
<template>
  <div class="p-8 text-center">
    <h2 class="text-3xl mb-4">Login</h2>
    <input placeholder="Email" class="p-2 m-2 w-64" />
    <input type="password" placeholder="Password" class="p-2 m-2 w-64" />
    <br />
    <button>Login</button>
  </div>
</template>



  
