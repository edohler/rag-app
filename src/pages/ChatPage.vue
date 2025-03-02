<template>
  <div class="chat-page">
    <div ref="messagesContainer" class="messages">
      <div v-for="(msg, index) in messages" :key="index" class="message-container">
        <div
          class="message"
          :class="{ 'user-message': msg.sender === 'User', 'ai-message': msg.sender === 'AI' }"
        >
          <!-- {{ msg.message }} -->
          <div
            v-if="msg.sender === 'AI'"
            v-html="renderMarkdown(msg.message)"
            class="ai-response"
          ></div>
          <div v-else>{{ msg.message }}</div>

          <!-- Display sources if AI message -->
          <div v-if="msg.sender === 'AI' && msg.sources.length" class="sources">
            <strong>Sources:</strong>
            <ul>
              <li v-for="(source, i) in msg.sources" :key="i">
                <a href="#" @click="openPdf(source, msg.content[i])">{{ source }}</a>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
    <!-- Right Sidebar -->
    <div v-if="selectedPdf" class="right-sidebar">
      <div class="pdfviewer-container">
        <PdfViewer :pdfPath="selectedPdf" :searchText="searchText" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick } from 'vue'
import { useChatStore } from '../stores/chatStore'
import { useRoute } from 'vue-router'
import { marked } from 'marked'
import PdfViewer from './PdfViewer.vue'

const chatStore = useChatStore()
const messages = computed(() => chatStore.messages)
const route = useRoute()
const messagesContainer = ref(null)

const selectedPdf = ref(null)
const searchText = ref('')

const openPdf = (filePath, content) => {
  selectedPdf.value = filePath
  // Extract the first few words from the matched content for searching
  if (content) {
    const words = content.split(' ')
    searchText.value = words.slice(0, 4).join(' ') // Take the first 4 words
  }
}

// Function to render Markdown safely
const renderMarkdown = (text) => {
  return marked.parse(text)
}

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

/* Styling of markdown AI response */
.ai-response h1 {
  font-size: 1.2em !important; /* Smaller than default */
  margin-bottom: 4px !important;
  font-weight: bold !important;
}

.ai-response h2 {
  font-size: 1.1em !important;
  margin-bottom: 4px !important;
  font-weight: bold !important;
}

.ai-response h3 {
  font-size: 1em !important;
  margin-bottom: 2px !important;
  font-weight: bold !important;
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

/* Right Sidebar (Takes 50% when visible) */
.right-sidebar {
  width: 50%;
  background: #f5f5f5;
  padding: 16px;
}

.pdfviewer-container {
  flex: 1;
  border-left: 2px solid #ccc;
}
</style>
