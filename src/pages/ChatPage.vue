<template>
  <div class="chat-page">
    <div ref="messagesContainer" class="messages">
      <div v-for="(msg, index) in messages" :key="index" class="message-container">
        <div
          class="message"
          :class="{ 'user-message': msg.sender === 'User', 'ai-message': msg.sender === 'AI' }"
        >
          {{ msg.message }}

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
import { ref, computed, watch, nextTick } from 'vue'
import { useChatStore } from '../stores/chatStore'
import { useRoute } from 'vue-router'

const chatStore = useChatStore()
const messages = computed(() => chatStore.messages)
const route = useRoute()
const messagesContainer = ref(null)

// Function to scroll to the bottom
const scrollToBottom = () => {
  console.log('Scrolling to bottom')
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

// Watch for new messages and scroll down
watch(
  messages,
  () => {
    scrollToBottom()
  },
  { deep: true },
)

// Watch for changes in the route ID and fetch messages accordingly
watch(
  () => route.params.id,
  async (newChatId) => {
    if (newChatId) {
      chatStore.chatId = newChatId // Update chat ID in store
      await chatStore.fetchMessages(newChatId)
    }
  },
  { immediate: true }, // This ensures it runs immediately when the component is mounted
)
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
  display: flex;
  flex-direction: column;
}

/* Container for each message */
.message-container {
  width: 100%;
  display: flex;
  flex-direction: column; /* Stack messages vertically */
}

/* Message Styling */
.message {
  display: flex;
  padding: 8px 12px;
  border-radius: 8px;
  word-wrap: break-word;
  overflow-wrap: break-word;
  width: fit-content;
  max-width: 70%;
  margin-bottom: 8px;
}

.user-message {
  align-self: flex-end;
  background: #007bff;
  color: white;
  text-align: right;
  max-width: 70%;
  justify-content: flex-end;
}

.ai-message {
  flex-direction: column;
  align-self: flex-start;
  background: #f1f1f1;
  color: black;
  text-align: left;
  max-width: 70%;
  justify-content: flex-start;
}

/* Source Styling */
.sources {
  margin-top: 15px;
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
