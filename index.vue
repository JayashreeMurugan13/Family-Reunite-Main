<template>
  <div class="home-wrapper">
    <!-- Hero section with intro text -->
    <section class="hero">
      <div class="hero-overlay">
        <h1 class="title">Reuniting Families</h1>
        <p class="subtitle">Find your loved ones with our missing person tracker</p>
      </div>
    </section>

    <!-- Bottom navigation moved above procedure -->
    <section class="bottom-nav">
      <NuxtLink to="/search" class="nav-box search">🔍 Search Person</NuxtLink>
      <NuxtLink to="/report" class="nav-box report">📢 Report Person</NuxtLink>
    </section>

    <!-- Simple procedure section -->
    <section class="procedure">
      <h2 class="section-title">How It Works</h2>
      <div class="steps">
        <div class="step" v-for="(step, i) in steps" :key="i">
          <h3>{{ step.title }}</h3>
          <p>{{ step.desc }}</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
 const router = useRouter()
router.replace('/login')

const steps = [
  { title: "1. Search", desc: "Browse or search through reported persons and found individuals." },
  { title: "2. Report", desc: "Submit missing person details including name, photo, and last seen location." },
  { title: "3. Connect", desc: "Contact authorities or listed family once someone is identified." },
  { title: "4. Reunite", desc: "Bring families back together and update the case status." }
]
</script>

<style scoped>
.home-wrapper {
  font-family: 'Georgia', serif;
  color: #2d3748;
  padding: 2rem;
  background-color: #f4f6f9;
}

.hero {
  background: #2c5364;
  padding: 4rem 2rem;
  text-align: center;
  border-radius: 1rem;
  margin-bottom: 3rem;
}

.hero-overlay .title {
  font-size: 3rem;
  color: white;
  margin-bottom: 1rem;
}

.hero-overlay .subtitle {
  font-size: 1.2rem;
  color: #e2e8f0;
}

.procedure {
  text-align: center;
  margin: 4rem 0;
}

.section-title {
  font-size: 2rem;
  margin-bottom: 2rem;
  color: #2c5364;
}

.steps {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 2rem;
}

.step {
  background: #ffffff;
  padding: 1.5rem;
  border-radius: 1rem;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
  transition: box-shadow 0.3s ease;
}

.step:hover {
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
}

.bottom-nav {
  display: flex;
  justify-content: center;
  gap: 2rem;
  margin-top: 3rem;
  margin-bottom: 4rem;
}

.nav-box {
  padding: 1.5rem 2.5rem;
  background: #2c5364;
  color: white;
  border-radius: 1rem;
  font-weight: bold;
  text-align: center;
  text-decoration: none;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
  transition: transform 0.3s ease, background 0.3s ease;
}

.nav-box:hover {
  transform: scale(1.05);
  background: #244652;
}
</style>
