<template>
    <div class="events-page">
      <section class="hero">
        <div class="overlay">
          <h1 class="hero-title">Our Work in Action</h1>
          <p class="hero-subtitle">Real stories, real reunions. Here's how we reconnect families.</p>
        </div>
      </section>
  
      <section class="event-grid">
        <div
          v-for="(activity, index) in activities"
          :key="index"
          class="event-card"
          :style="`animation-delay: ${index * 0.2}s`"
        >
          <img :src="activity.image" alt="activity photo" class="event-img" />
          <h3>{{ activity.title }}</h3>
          <p>{{ activity.description }}</p>
          <NuxtLink to="/contact" class="learn-more">Contact Us</NuxtLink>
        </div>
      </section>
    </div>
  </template>
  
  <script setup>
  const activities = [
    {
      title: 'Awareness Campaigns',
      description: 'We conduct public awareness programs in schools, communities, and media to spread information.',
      image: '/images/awareness.jpg',
    },
    {
      title: 'Field Volunteer Search',
      description: 'Our team conducts field operations in locations where missing persons were last seen.',
      image: '/images/volunteer.jpg',
    },
    {
      title: 'Technology-Based Matching',
      description: 'We use facial recognition and database matching to connect found individuals with families.',
      image: '/images/tech-match.jpg',
    },
    {
      title: 'Family Reunification Events',
      description: 'We host reunification events where families are brought together in emotional reunions.',
      image: '/images/reunion-event.jpg',
    },
  ]
  </script>
  
  <style scoped>
  .events-page {
    font-family: 'Georgia', serif;
    color: #222;
  }
  
  .hero {
    background: url('/images/events-hero.jpg') no-repeat center center/cover;
    height: 60vh;
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    animation: fadeIn 2s ease-in-out;
  }
  
  .overlay {
    background: rgba(0, 0, 0, 0.6);
    padding: 2rem;
    text-align: center;
    color: white;
    border-radius: 1rem;
    animation: slideUp 1.5s ease-in-out;
  }
  
  .hero-title {
    font-size: 3rem;
    animation: fadeInDown 1.5s;
  }
  
  .hero-subtitle {
    font-size: 1.2rem;
    animation: fadeInUp 2s;
  }
  
  .event-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 2rem;
    padding: 3rem;
  }
  
  .event-card {
    background: #fff;
    border-radius: 1rem;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
    overflow: hidden;
    padding: 1rem;
    text-align: center;
    animation: bounceInUp 1s forwards;
  }
  
  .event-img {
    width: 100%;
    height: 200px;
    object-fit: cover;
    border-radius: 0.5rem;
    margin-bottom: 1rem;
    transition: transform 0.4s ease;
  }
  
  .event-card:hover .event-img {
    transform: scale(1.05);
  }
  
  .learn-more {
    margin-top: 1rem;
    display: inline-block;
    background: #ff6f61;
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 2rem;
    font-weight: bold;
    text-decoration: none;
    transition: background 0.3s;
  }
  
  .learn-more:hover {
    background: #e2554f;
  }
  
  /* Animations */
  @keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
  }
  
  @keyframes slideUp {
    from { transform: translateY(100px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
  }
  
  @keyframes fadeInDown {
    from { opacity: 0; transform: translateY(-50px); }
    to { opacity: 1; transform: translateY(0); }
  }
  
  @keyframes fadeInUp {
    from { opacity: 0; transform: translateY(50px); }
    to { opacity: 1; transform: translateY(0); }
  }
  
  @keyframes bounceInUp {
    0% {
      opacity: 0;
      transform: translateY(200px);
    }
    60% {
      opacity: 1;
      transform: translateY(-20px);
    }
    80% {
      transform: translateY(10px);
    }
    100% {
      transform: translateY(0);
    }
  }
  </style>
  
