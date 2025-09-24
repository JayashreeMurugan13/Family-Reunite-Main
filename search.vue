<template>
  <div class="search-page">
    <!-- Main Content -->
    <section class="search-hero">
      <div class="overlay">
        <h1 class="title">Search for a Missing Person</h1>
        <p class="subtitle">Help reunite families by providing information</p>
      </div>
    </section>

    <section class="search-form-section">
      <form @submit.prevent="submitSearch" class="search-form">
        <div class="form-group">
          <label>Name of Missing Person:</label>
          <input type="text" v-model="form.name">
        </div>

        <div class="form-group">
          <label>Age:</label>
          <input type="number" v-model="form.age" required>
        </div>

        <div class="form-group">
          <label>Gender:</label>
          <select v-model="form.gender" required>
            <option value="">Select Gender</option>
            <option value="male">Male</option>
            <option value="female">Female</option>
            <option value="other">Other</option>
          </select>
        </div>

        <div class="form-group">
          <label>Last Seen Location:</label>
          <input type="text" v-model="form.lastSeen" required>
        </div>

        <div class="form-group">
          <label>Date and Time Last Seen:</label>
          <input type="datetime-local" v-model="form.datetime" required>
        </div>

        <div class="form-group">
          <label>Dress Color:</label>
          <input type="text" v-model="form.dressColor">
        </div>

        <div class="form-group">
          <label>Hair Color:</label>
          <input type="text" v-model="form.hairColor">
        </div>

        <div class="form-group">
          <label>Height (cm):</label>
          <input type="number" v-model="form.height">
        </div>

        <div class="form-group">
          <label>Weight (kg):</label>
          <input type="number" v-model="form.weight">
        </div>

        <div class="form-group">
          <label>Face Complexion:</label>
          <input type="text" v-model="form.faceColor">
        </div>

        <div class="form-group">
          <label>Upload Photo:</label>
          <input type="file" @change="handlePhoto" accept="image/*" required>
        </div>

        <div class="form-group">
          <label>Additional Details:</label>
          <textarea v-model="form.details" rows="4"></textarea>
        </div>

        <div class="form-group">
          <button type="submit" :disabled="isSubmitting">
            {{ isSubmitting ? 'Searching...' : 'Search' }}
          </button>
        </div>
      </form>

      <!-- Results Section -->
      <div v-if="matches.length > 0" class="results-section">
        <h2>Search Results ({{ matches.length }} matches found)</h2>
        <div class="match-grid">
          <div v-for="match in matches" :key="match.report_id" class="match-card">
            <img :src="getPhotoUrl(match.photo_url)" :alt="match.name" class="match-photo">
            <div class="match-details">
              <h3>{{ match.name }}</h3>
              <p><strong>Age:</strong> {{ match.age }}</p>
              <p><strong>Gender:</strong> {{ match.gender }}</p>
              <p><strong>Last Seen:</strong> {{ match.last_seen }}</p>
              <p><strong>Match Confidence:</strong> {{ (match.confidence * 100).toFixed(1) }}%</p>
              <button @click="viewDetails(match.report_id)" class="view-details-btn">
                View Details
              </button>
            </div>
          </div>
        </div>
      </div>

      <div v-else-if="searchPerformed" class="no-results">
        <p>No matching reports found. Try adjusting your search criteria.</p>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const form = ref({
  name: '',
  age: '',
  gender: '',
  lastSeen: '',
  datetime: '',
  dressColor: '',
  hairColor: '',
  height: '',
  weight: '',
  faceColor: '',
  photo: null,
  details: ''
})

const matches = ref([])
const isSubmitting = ref(false)
const searchPerformed = ref(false)

const api = axios.create({
  baseURL: 'http://localhost:8003'
})

const handlePhoto = (e) => {
  form.value.photo = e.target.files[0]
}

const getPhotoUrl = (path) => {
  // In production, you would use a proper URL
  return path ? `http://localhost:8003/${path}` : ''
}
const submitSearch = async () => {
  isSubmitting.value = true
  searchPerformed.value = false
  matches.value = []
  
  try {
    const formData = new FormData()
    
    // Convert datetime to ISO string if it exists
    if (form.value.datetime) {
      formData.append('datetime', new Date(form.value.datetime).toISOString())
    }
    
    // Append other form fields
    Object.entries(form.value).forEach(([key, value]) => {
      if (value !== null && value !== '' && key !== 'datetime') {
        if (key === 'photo') {
          if (value) formData.append(key, value)
        } else {
          formData.append(key.replace(/([A-Z])/g, '_$1').toLowerCase(), value)
        }
      }
    })

    const token = localStorage.getItem('auth_token')
    const response = await api.post('/api/search', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
        'Authorization': `Bearer ${token}`
      }
    })
    
    matches.value = response.data
    searchPerformed.value = true
    
  } catch (error) {
    const msg = error.response?.data?.detail ||
                error.response?.data?.message ||
                'Search failed. Please try again.'
    alert(msg)
  } finally {
    isSubmitting.value = false
  }
}

const viewDetails = (reportId) => {
  // Navigate to report details page
  console.log('Viewing details for report:', reportId)
  // In a real app: router.push(`/reports/${reportId}`)
}
</script>

<style scoped>
.search-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.search-hero {
  background: url('https://via.placeholder.com/1200x400') center/cover;
  height: 400px;
  border-radius: 8px;
  margin-bottom: 2rem;
  position: relative;
}

.overlay {
  background: rgba(0, 0, 0, 0.5);
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: white;
  border-radius: 8px;
  text-align: center;
}

.title {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.subtitle {
  font-size: 1.2rem;
  max-width: 600px;
}

.search-form-section {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.search-form {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 600;
}

.form-group input,
.form-group select,
.form-group textarea {
  padding: 0.8rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 1rem;
}

.form-group textarea {
  resize: vertical;
}

.form-group button {
  background: #007bff;
  color: white;
  padding: 1rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  transition: background 0.3s ease;
  grid-column: span 2;
}

.form-group button:disabled {
  background: #6c757d;
  cursor: not-allowed;
}

.form-group button:hover:not(:disabled) {
  background: #0056b3;
}

.results-section {
  margin-top: 3rem;
  grid-column: 1 / -1;
}

.results-section h2 {
  margin-bottom: 1.5rem;
  font-size: 1.8rem;
  color: #333;
  border-bottom: 2px solid #eee;
  padding-bottom: 0.5rem;
}

.match-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.match-card {
  border: 1px solid #ddd;
  border-radius: 8px;
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.match-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.match-photo {
  width: 100%;
  height: 250px;
  object-fit: cover;
}

.match-details {
  padding: 1.2rem;
}

.match-details h3 {
  margin-top: 0;
  margin-bottom: 0.8rem;
  font-size: 1.3rem;
  color: #007bff;
}

.match-details p {
  margin: 0.5rem 0;
  font-size: 0.95rem;
}

.view-details-btn {
  background: #28a745;
  color: white;
  border: none;
  padding: 0.6rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 1rem;
  width: 100%;
  transition: background 0.3s ease;
}

.view-details-btn:hover {
  background: #218838;
}

.no-results {
  grid-column: 1 / -1;
  text-align: center;
  padding: 2rem;
  background: #f8f9fa;
  border-radius: 8px;
  margin-top: 2rem;
}

.no-results p {
  font-size: 1.1rem;
  color: #6c757d;
}

@media (max-width: 768px) {
  .search-form {
    grid-template-columns: 1fr;
  }
  
  .form-group button {
    grid-column: 1;
  }
}
</style>
