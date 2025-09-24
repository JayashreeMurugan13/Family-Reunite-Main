<template>
  <div class="gallery-page">
    <section class="hero">
      <div class="overlay">
        <h1 class="title">Family Gallery</h1>
        <p class="subtitle">Every report brings us closer to a reunion.</p>
      </div>
    </section>

    <section class="grid">
      <div
        v-for="(person, index) in reportedPersons"
        :key="index"
        class="card"
        :style="{ animationDelay: `${index * 0.2}s` }"
      >
        <img :src="person.photo" alt="Missing Person" class="photo" />
        <div class="info">
          <h3>{{ person.name }}</h3>
          <p><strong>Date Missing:</strong> {{ person.date }}</p>
          <p><strong>Last Seen:</strong> {{ person.location }}</p>
          <p><strong>Dress:</strong> {{ person.dressColor }}</p>
          <p><strong>Hair:</strong> {{ person.hairColor }}</p>
          <p><strong>Height:</strong> {{ person.height }} cm</p>
          <p><strong>Weight:</strong> {{ person.weight }} kg</p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
const reportedPersons = [
  {
    name: 'John Doe',
    date: '2025-04-01',
    location: 'Chennai Central',
    dressColor: 'Blue Shirt, Black Jeans',
    hairColor: 'Black',
    height: 170,
    weight: 65,
    photo: '/images/report1.jpg',
  },
  {
    name: 'Meena Kumari',
    date: '2025-03-28',
    location: 'Coimbatore Junction',
    dressColor: 'Green Saree',
    hairColor: 'Brown',
    height: 160,
    weight: 55,
    photo: '/images/report2.jpg',
  },
]
</script>

<style scoped>
.gallery-page {
  font-family: 'Georgia', serif;
  color: #222;
  background: #f5f7fa;
}

.hero {
  background: url('/images/gallery-hero.jpg') no-repeat center center/cover;
  height: 60vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}

.overlay {
  background-color: rgba(0, 0, 0, 0.5);
  padding: 2rem;
  border-radius: 1rem;
  color: #fff;
  text-align: center;
  animation: slideFadeIn 1.5s ease-in-out forwards;
}

.title {
  font-size: 3rem;
  margin-bottom: 1rem;
  animation: fadeInUp 1.5s ease-in-out forwards;
}

.subtitle {
  font-size: 1.2rem;
  animation: fadeIn 2s ease-in;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
  padding: 3rem;
  animation: fadeIn 2s ease-in;
}

.card {
  background: #fff;
  border-radius: 1rem;
  overflow: hidden;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  transform: translateY(50px);
  animation: bounceInUp 1s forwards;
}

.photo {
  width: 100%;
  height: 250px;
  object-fit: cover;
}

.info {
  padding: 1rem;
  text-align: left;
}

/* Animations */                                      
@keyframes slideFadeIn {
  from { opacity: 0; transform: translateY(50px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

@keyframes fadeInUp {
  from { transform: translateY(30px); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}

@keyframes bounceInUp {
  0% { transform: translateY(100px); opacity: 0; }
  60% { transform: translateY(-20px); opacity: 1; }
  80% { transform: translateY(10px); }
  100% { transform: translateY(0); }
}
</style>
