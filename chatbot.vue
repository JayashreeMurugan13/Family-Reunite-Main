<template>
  <div class="chatbot-page">
    <section class="chat-header">
      <h1>Ask Us Anything!</h1>
      <p>We are here to help you find your loved ones. Type your query below.</p>
    </section>

    <div class="chatbox">
      <div class="messages">
        <div
          v-for="(msg, index) in messages"
          :key="index"
          :class="['message', msg.sender]"
        >
          {{ msg.text }}
        </div>
      </div>

      <form @submit.prevent="sendMessage" class="input-form">
        <input
          v-model="newMessage"
          type="text"
          placeholder="Type your question..."
          required
        />
        <button type="submit">Send</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const messages = ref([
  { text: 'Hello! How can I assist you today?', sender: 'bot' }
])

const newMessage = ref('')

function sendMessage() {
  if (newMessage.value.trim() !== '') {
    messages.value.push({ text: newMessage.value, sender: 'user' })

    // Simulate bot response
    setTimeout(() => {
      messages.value.push({
        text: 'Thank you for your message. Our team will reach out shortly.',
        sender: 'bot'
      })
    }, 1000)

    newMessage.value = ''
  }
}
</script>

<style scoped>
.chatbot-page {
  padding: 2rem;
  font-family: 'Georgia', serif;
  background: #f5f7fa;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.chat-header {
  text-align: center;
  margin-bottom: 2rem;
  animation: fadeInDown 1.5s;
}

.chatbox {
  width: 100%;
  max-width: 600px;
  background: white;
  border-radius: 1rem;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
  padding: 1rem;
  display: flex;
  flex-direction: column;
  animation: fadeInUp 2s;
}

.messages {
  flex: 1;
  max-height: 400px;
  overflow-y: auto;
  margin-bottom: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.message {
  padding: 0.7rem 1rem;
  border-radius: 1rem;
  max-width: 75%;
  word-wrap: break-word;
  animation: fadeIn 0.5s ease-in;
}

.message.bot {
  background: #e9f5ff;
  align-self: flex-start;
}

.message.user {
  background: #d1ffd6;
  align-self: flex-end;
}

.input-form {
  display: flex;
  gap: 1rem;
}

.input-form input {
  flex: 1;
  padding: 0.7rem 1rem;
  border: 1px solid #ccc;
  border-radius: 2rem;
  font-size: 1rem;
}

.input-form button {
  background: #007bff;
  color: white;
  border: none;
  padding: 0.7rem 1.5rem;
  border-radius: 2rem;
  cursor: pointer;
  transition: background 0.3s;
}

.input-form button:hover {
  background: #0056b3;
}

@keyframes fadeInDown {
  from { opacity: 0; transform: translateY(-20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes fadeInUp {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
</style>

  