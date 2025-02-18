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

        <!-- New History Item -->
        <q-item clickable v-ripple @click="toggleHistory">
          <q-item-section avatar>
            <q-icon name="history" />
          </q-item-section>
          <q-item-section>
            <q-item-label>History</q-item-label>
          </q-item-section>
        </q-item>

        <!-- Chat History Items -->
        <q-list v-if="showHistory" class="history-list">
          <q-item
            v-for="chat in chatStore.chatHistory"
            :key="chat.id"
            clickable
            v-ripple
            @click="openChat(chat.id)"
          >
            <!-- <q-item-section avatar>
              <q-icon name="chat" />
            </q-item-section> -->
            <q-item-section>
              <q-item-label>{{ chat.title }}</q-item-label>
            </q-item-section>
          </q-item>
        </q-list>
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
            @keyup.enter="handleSendMessage"
          />
          <q-btn round flat icon="send" @click="handleSendMessage" />
        </q-toolbar>
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useChatStore } from '../stores/chatStore'

const router = useRouter()
const chatStore = useChatStore()
const showLeftSidebar = ref(true)
const rightDrawerOpen = ref(true)
const newQuestion = ref('')
const showHistory = ref(false)

const openChat = (id) => {
  console.log('Navigating to chat:', id)
  chatStore.chatId = id // Update store with selected chat
  router.push(`/chat/${id}`) // Navigate to ChatPage.vue
}

const handleSendMessage = () => {
  if (!newQuestion.value.trim()) return
  chatStore.sendMessage(newQuestion.value)
  // console.log('Sending message:', newQuestion.value)
  newQuestion.value = '' // Reset input after sending
}

const toggleHistory = () => {
  showHistory.value = !showHistory.value
}

onMounted(chatStore.fetchChatHistory)
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
  max-width: calc(100% - 300px);
  transition: all 0.3s ease-in-out;
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

/* History List Padding */
.history-list {
  padding-left: 16px;
}
</style>
