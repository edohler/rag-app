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
          v-for="chat in chatStore.chatHistory"
          :key="chat.id"
          clickable
          v-ripple
          @click="chatStore.fetchMessages(chat.id)"
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
            @keyup.enter="
              chatStore.sendMessage(newQuestion)
              newQuestion = ''
            "
          />
          <q-btn
            round
            flat
            icon="send"
            @click="
              chatStore.sendMessage(newQuestion)
              newQuestion = ''
            "
          />
        </q-toolbar>
      </div>
    </div>
  </q-page>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useChatStore } from '@/stores/chatStore'

const chatStore = useChatStore()
const showLeftSidebar = ref(true)
const rightDrawerOpen = ref(true)
const newQuestion = ref('')

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
