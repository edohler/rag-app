<template>
  <q-page class="row full-height">
    <!-- Left Sidebar -->
    <div v-if="showLeftSidebar" class="left-sidebar">
      <q-list>
        <q-item-label header> Chatbot Settings </q-item-label>

        <q-item clickable v-ripple>
          <q-item-section avatar>
            <q-icon name="tune" />
          </q-item-section>
          <q-item-section>
            <q-item-label>Adjust Model Settings</q-item-label>
          </q-item-section>
        </q-item>

        <q-item
          v-for="chat in chatHistory"
          :key="chat.id"
          clickable
          v-ripple
          :to="`/chat/${chat.id}`"
        >
          <q-item-section avatar>
            <q-icon name="history" />
          </q-item-section>
          <q-item-section>
            <q-item-label>{{ chat.title }}</q-item-label>
          </q-item-section>
        </q-item>
      </q-list>
    </div>

    <div class="content-wrapper">
      <div class="chat-wrapper">
        <!-- Main Chat Content -->
        <div class="chat-container">
          <router-view />
        </div>

        <!-- Right Sidebar -->
        <div v-if="rightDrawerOpen" class="right-sidebar">
          <q-list>
            <q-item-label header>File Preview</q-item-label>
            <q-item>
              <q-item-section>
                <q-item-label>No file selected yet</q-item-label>
              </q-item-section>
            </q-item>
          </q-list>
        </div>
      </div>

      <div class="chat-footer">
        <q-toolbar class="row justify-between">
          <q-btn round flat icon="insert_emoticon" class="q-mr-sm" />
          <q-input
            rounded
            outlined
            dense
            class="col-grow q-mr-sm"
            bg-color="white"
            v-model="newQuestion"
            placeholder="Type a question"
            @keyup.enter="sendMessage"
          />
          <q-btn round flat icon="send" @click="sendMessage" />
        </q-toolbar>
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const showLeftSidebar = ref(true) // Only shown on this page
const rightDrawerOpen = ref(true) // Opens dynamically

const chatHistory = ref([
  { id: '123', title: 'Chat with AI' },
  { id: '456', title: 'RAG Test' },
])
const chatId = '123' // Static chat ID for now

const newQuestion = ref('')
const messages = ref([{ sender: 'ai', text: 'Hello! How can I help?' }])

const sendMessage = async () => {
  if (!newQuestion.value.trim()) return

  const res = await axios.post(`http://127.0.0.1:8000/chats/${chatId}`, {
    sender: 'User',
    message: newQuestion.value.trim(),
  })

  messages.value.push(res.data) // Show AI response
  newQuestion.value = '' // Clear input
}
</script>

<style scoped>
/* Sidebar Styling */
.left-sidebar {
  width: 300px;
  background: #f5f5f5;
  padding: 16px;
}

/* Content Wrapper (Main + Right Sidebar) */
.content-wrapper {
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  transition: all 0.3s ease-in-out;
  /* flex-direction: column; */
}

.chat-wrapper {
  display: flex;
  flex-grow: 1;
}

/* Main Content (Shrinks if right sidebar opens) */
.chat-container {
  flex-grow: 1;
  padding: 16px;
  transition: width 0.3s ease-in-out;
  overflow: auto;
}
.chat-container.half-width {
  width: 50%;
}

/* Right Sidebar (Takes 50% when visible) */
.right-sidebar {
  width: 50%;
  background: #f5f5f5;
  padding: 16px;
}

/* Footer Styling */
.chat-footer {
  height: 66px;
  bottom: 0;
  left: 300px;
  right: 0;
  background: #ddd;
  padding: 8px;
  display: flex;
  gap: 8px;
}
</style>
