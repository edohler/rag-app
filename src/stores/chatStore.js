import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'
import { v4 as uuidv4 } from 'uuid' // For generating new chat IDs

export const useChatStore = defineStore('chat', () => {
  const chatId = ref(null) // Current chat ID
  const messages = ref([]) // Messages for active chat
  const chatHistory = ref([]) // List of past chats

  // Load chat history for sidebar
  const fetchChatHistory = async () => {
    const res = await axios.get('http://127.0.0.1:8000/chats')
    chatHistory.value = res.data // [{ id: '123', title: 'Chat 1' }, { id: '456', title: 'RAG Test' }]
  }

  // Load messages for selected chat
  const fetchMessages = async (id) => {
    chatId.value = id
    const res = await axios.get(`http://127.0.0.1:8000/chats/${id}`)
    messages.value = res.data
  }

  // Send new message
  const sendMessage = async (text) => {
    if (!text.trim()) return

    // If no chat ID, create a new chat
    if (!chatId.value) {
      chatId.value = uuidv4()
    }

    // Add user's message locally
    messages.value.push({ sender: 'User', text })

    // Send to backend
    const res = await axios.post(`http://127.0.0.1:8000/chats/${chatId.value}`, {
      sender: 'User',
      message: text.trim(),
    })

    // Store AI response with sources
    messages.value.push({
      sender: 'AI',
      message: res.data.message,
      sources: res.data.sources || [],
      content: res.data.content || [],
    })
  }

  return { chatId, messages, chatHistory, fetchChatHistory, fetchMessages, sendMessage }
})
