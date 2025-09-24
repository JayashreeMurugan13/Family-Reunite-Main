<template>
  <div class="report-page">
    <!-- Hero Section -->
    <section class="report-hero">
      <div class="overlay">
        <h1 class="title">Report Missing Person</h1>
        <p class="subtitle">Provide details to help reunite your loved ones</p>
      </div>
    </section>

    <!-- Form Section -->
    <section class="report-form-section">
      <form @submit.prevent="submitReport" class="report-form">
        <div class="form-group">
          <label>Full Name</label>
          <input v-model="form.name" type="text" required />
        </div>

        <div class="form-group">
          <label>Age</label>
          <input v-model="form.age" type="number" min="1" max="120" required />
        </div>

        <div class="form-group">
          <label>Gender</label>
          <select v-model="form.gender" required>
            <option value="" disabled>Select Gender</option>
            <option value="male">Male</option>
            <option value="female">Female</option>
            <option value="other">Other</option>
          </select>
        </div>

        <div class="form-group">
          <label>Last Seen Location</label>
          <input v-model="form.lastSeen" type="text" required />
        </div>

        <div class="form-group">
          <label>Date & Time Last Seen</label>
          <input v-model="form.datetime" type="datetime-local" required />
        </div>

        <div class="form-group">
          <label>Dress Color</label>
          <input v-model="form.dressColor" type="text" />
        </div>

        <div class="form-group">
          <label>Hair Color</label>
          <input v-model="form.hairColor" type="text" />
        </div>

        <div class="form-group">
          <label>Height (cm)</label>
          <input v-model="form.height" type="number" min="30" max="250" />
        </div>

        <div class="form-group">
          <label>Weight (kg)</label>
          <input v-model="form.weight" type="number" min="5" max="300" />
        </div>

        <div class="form-group">
          <label>Face Complexion</label>
          <input v-model="form.faceColor" type="text" />
        </div>

        <div class="form-group">
          <label>Photo</label>
          <input 
            type="file" 
            @change="handlePhoto" 
            accept="image/*" 
            required
            ref="photoInput"
          />
          <small v-if="form.photo" class="file-name">
            Selected file: {{ form.photo.name }}
          </small>
        </div>

        <div class="form-group">
          <label>Additional Details</label>
          <textarea 
            v-model="form.details" 
            rows="4"
            placeholder="Any distinctive features, last seen clothing, etc."
          ></textarea>
        </div>

        <div class="form-group">
          <button 
            type="submit" 
            :disabled="isSubmitting"
            class="submit-btn"
          >
            <span v-if="!isSubmitting">Submit Report</span>
            <span v-else>Submitting...</span>
          </button>
          <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
          <p v-if="successMessage" class="success-message">{{ successMessage }}</p>
        </div>
      </form>
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

const isSubmitting = ref(false)
const errorMessage = ref('')
const successMessage = ref('')
const photoInput = ref(null)

const api = axios.create({
  baseURL: 'http://localhost:8000', // Match your backend URL
  timeout: 10000
})

const handlePhoto = (e) => {
  const file = e.target.files[0]
  if (file) {
    if (!['image/jpeg', 'image/png'].includes(file.type)) {
      errorMessage.value = 'Only JPG/PNG files allowed'
      photoInput.value.value = ''
      return
    }
    if (file.size > 5 * 1024 * 1024) { // 5MB limit
      errorMessage.value = 'File size must be less than 5MB'
      photoInput.value.value = ''
      return
    }
    form.value.photo = file
    errorMessage.value = ''
  }
}

const submitReport = async () => {
  errorMessage.value = ''
  successMessage.value = ''
  isSubmitting.value = true

  try {
    const formData = new FormData()
    
    // Convert camelCase to snake_case for backend
    const fields = {
      name: 'name',
      age: 'age',
      gender: 'gender',
      lastSeen: 'last_seen',
      datetime: 'datetime_str',
      dressColor: 'dress_color',
      hairColor: 'hair_color',
      height: 'height',
      weight: 'weight',
      faceColor: 'face_color',
      details: 'details',
      photo: 'photo'
    }

    // Append all form data
    Object.entries(fields).forEach(([frontendKey, backendKey]) => {
      const value = form.value[frontendKey]
      if (value !== null && value !== '') {
        if (frontendKey === 'datetime') {
          // Convert to ISO string without milliseconds
          formData.append(backendKey, new Date(value).toISOString().slice(0, 16))
        } else if (frontendKey === 'photo') {
          if (value) formData.append(backendKey, value)
        } else {
          formData.append(backendKey, value)
        }
      }
    })

    const response = await api.post('/api/reports/submit', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })

    if (response.data.status === 'success') {
      successMessage.value = 'Report submitted successfully!'
      resetForm()
    }
    
  } catch (error) {
    console.error('Submission error:', error)
    errorMessage.value = error.response?.data?.detail || 
                        error.response?.data?.message || 
                        'Failed to submit report. Please try again.'
  } finally {
    isSubmitting.value = false
  }
}

const resetForm = () => {
  form.value = {
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
  }
  photoInput.value.value = ''
}
</script>

<style scoped>
.report-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.report-hero {
  background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)),
              url('https://source.unsplash.com/random/1200x400?missing') center/cover;
  height: 400px;
  border-radius: 12px;
  margin-bottom: 2rem;
  position: relative;
}

.overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: white;
  text-align: center;
  padding: 0 20px;
}

.title {
  font-size: 2.8rem;
  margin-bottom: 1rem;
  font-weight: 700;
}

.subtitle {
  font-size: 1.2rem;
  max-width: 600px;
  opacity: 0.9;
}

.report-form-section {
  background: #ffffff;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.report-form {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

label {
  font-weight: 600;
  color: #2d3748;
}

input, select, textarea {
  padding: 0.8rem 1rem;
  border: 1px solid #e2e8f0;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.2s;
}

input:focus, select:focus, textarea:focus {
  outline: none;
  border-color: #4299e1;
  box-shadow: 0 0 0 3px rgba(66, 153, 225, 0.2);
}

textarea {
  resize: vertical;
  min-height: 100px;
}

.submit-btn {
  grid-column: 1 / -1;
  padding: 1rem 2rem;
  background-color: #4299e1;
  color: white;
  border: none;
  border-radius: 6px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.2s;
}

.submit-btn:disabled {
  background-color: #a0aec0;
  cursor: not-allowed;
}

.submit-btn:hover:not(:disabled) {
  background-color: #3182ce;
}

.error-message {
  color: #e53e3e;
  margin-top: 1rem;
  text-align: center;
}

.success-message {
  color: #38a169;
  margin-top: 1rem;
  text-align: center;
}

.file-name {
  color: #718096;
  font-size: 0.9rem;
  margin-top: 0.5rem;
}

@media (max-width: 768px) {
  .report-form {
    grid-template-columns: 1fr;
  }
  
  .title {
    font-size: 2rem;
  }
  
  .subtitle {
    font-size: 1rem;
  }
}
</style>
