<template>
  <div class="chat-page">
    <div class="messages">
      <div v-for="(msg, index) in messages" :key="index" :class="msg.sender">
        <div
          class="message"
          :class="{ 'user-message': msg.sender === 'User', 'ai-message': msg.sender === 'AI' }"
        >
          {{ msg.text }}

          <!-- Display sources if AI message -->
          <div v-if="msg.sender === 'AI' && msg.sources.length" class="sources">
            <strong>Sources:</strong>
            <ul>
              <li v-for="(source, i) in msg.sources" :key="i">
                <a :href="'file://' + source" target="_blank">{{ source }}</a>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useChatStore } from '@/stores/chatStore'

const chatStore = useChatStore()
const messages = ref(chatStore.messages)

onMounted(() => {
  if (chatStore.chatId) {
    chatStore.fetchMessages(chatStore.chatId)
  }
})
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

/* Message Styling */
.message {
  padding: 8px 12px;
  border-radius: 8px;
  max-width: 70%;
}

.user-message {
  align-self: flex-end;
  background: #007bff;
  color: white;
}

.ai-message {
  align-self: flex-start;
  background: #f1f1f1;
  color: black;
}

/* Source Styling */
.sources {
  margin-top: 5px;
  font-size: 0.9em;
  color: gray;
}

.sources ul {
  padding-left: 15px;
}

.sources a {
  color: #007bff;
  text-decoration: none;
}

.sources a:hover {
  text-decoration: underline;
}
</style>
