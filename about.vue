<template>
  <div class="about-page">
    <h1 class="page-title">About Our Family</h1>
    <p class="intro-text">
      Our journey is filled with stories, emotions, and a legacy that continues through generations.
    </p>

    <div class="card-section">
      <div class="info-card" v-for="(item, index) in cards" :key="index">
        <h3>{{ item.title }}</h3>
        <p>{{ item.description }}</p>
      </div>
    </div>

    <div class="quote">
      <blockquote>
        “Family is not an important thing. It's everything.” – Michael J. Fox
      </blockquote>
    </div>
  </div>
</template>

<script setup>
const cards = [
  {
    title: 'Our Roots',
    description: 'Tracing back generations, our family tree is rich with culture, love, and resilience.',
  },
  {
    title: 'Our Values',
    description: 'We believe in unity, support, and celebrating every member of our family.',
  },
  {
    title: 'Our Work',
    description: 'Through dedication and collective effort, we have successfully reunited many lost families across regions.',
  },
]
</script>

<style scoped>
.about-page {
  padding: 3rem 1rem;
  max-width: 1000px;
  margin: auto;
  font-family: 'Georgia', serif;
  animation: fadeInUp 1.5s ease-in;
  color: #2e2e2e;
}

.page-title {
  font-size: 2.8rem;
  color: #4a148c;
  text-align: center;
  margin-bottom: 1rem;
  animation: pulseTitle 2s infinite;
}

.intro-text {
  font-size: 1.2rem;
  text-align: center;
  margin-bottom: 3rem;
  line-height: 1.6;
  animation: fadeIn 2s ease-in;
}

.card-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.info-card {
  background: rgba(255, 255, 255, 0.9);
  padding: 2rem;
  border-radius: 1rem;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  transition: transform 0.4s ease, background 0.4s ease;
  animation: slideUp 1s ease forwards;
}

.info-card:hover {
  transform: translateY(-10px) scale(1.02);
  background: #f8eafc;
}

.info-card h3 {
  font-size: 1.5rem;
  color: #6a1b9a;
  margin-bottom: 0.5rem;
}

.info-card p {
  font-size: 1rem;
  color: #555;
}

.quote blockquote {
  font-style: italic;
  font-size: 1.2rem;
  color: #333;
  text-align: center;
  background: #f3e5f5;
  padding: 1.5rem;
  border-radius: 1rem;
  animation: fadeInQuote 1.5s ease-out;
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(40px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes slideUp {
  from { transform: translateY(50px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes pulseTitle {
  0%, 100% { transform: scale(1); color: #4a148c; }
  50% { transform: scale(1.03); color: #6a1b9a; }
}

@keyframes fadeInQuote {
  from { opacity: 0; transform: scale(0.95); }
  to { opacity: 1; transform: scale(1); }
}
</style>

  