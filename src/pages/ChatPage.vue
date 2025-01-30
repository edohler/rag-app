<template>
  <div class="chat-page">
    <div class="messages">
      <div v-for="(msg, index) in messages" :key="index" :class="msg.sender">
        {{ msg.text }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const messages = ref([])
const chatId = '123' // Static chat ID for now

// Fetch messages from local SQLite database
const fetchMessages = async () => {
  const res = await axios.get(`http://127.0.0.1:8000/chats/${chatId}`)
  messages.value = res.data
}

// Fetch messages on mount
onMounted(fetchMessages)
</script>

<style scoped>
.chat-page {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
}
.messages {
  flex-grow: 1;
  overflow-y: auto;
  padding: 16px;
}
.ai {
  background: #ddd;
  padding: 8px;
  border-radius: 8px;
  align-self: flex-start;
}
.user {
  background: #007aff;
  color: white;
  padding: 8px;
  border-radius: 8px;
  align-self: flex-end;
}
</style>
