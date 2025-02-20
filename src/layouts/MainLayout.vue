<template>
  <q-layout view="hHh lpR fFf">
    <q-header elevated class="bg-secondary text-white" height-hint="98">
      <q-toolbar>
        <q-toolbar-title>
          <q-avatar>
            <img src="https://cdn.quasar.dev/logo-v2/svg/logo-mono-white.svg" />
          </q-avatar>
          RAG - The open gate to the archive
        </q-toolbar-title>
      </q-toolbar>

      <q-tabs align="left">
        <q-route-tab to="/" label="Chat" />
        <q-route-tab to="/page2" label="Vector database" />
        <q-route-tab to="/page3" label="Help" />
      </q-tabs>
    </q-header>

    <q-page-container style="padding-top: 98px">
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { watch } from 'vue'
import { useChatStore } from 'stores/chatStore'

const route = useRoute()
const chatStore = useChatStore()

watch(
  () => route.path,
  (newPath) => {
    if (newPath === '/') {
      chatStore.chatId = null // Reset chat ID when navigating to "/"
      chatStore.messages = []
    }
  },
)
</script>
