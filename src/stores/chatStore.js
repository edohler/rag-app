import { defineStore } from 'pinia'
import { ref } from 'vue'
import axios from 'axios'
import { v4 as uuidv4 } from 'uuid' // For generating new chat IDs

const LOCAL_API = 'http://127.0.0.1:8000'

export const useChatStore = defineStore('chat', () => {
  const chatId = ref(null) // Current chat ID
  const messages = ref([]) // Messages for active chat
  const chatHistory = ref([]) // List of past chats

  // Load chat history for sidebar
  const fetchChatHistory = async () => {
    const res = await axios.get(`${LOCAL_API}/chats`)
    chatHistory.value = res.data
  }

  // Load messages for selected chat
  const fetchMessages = async (id) => {
    chatId.value = id
    try {
      console.log('Fetching messages for chat ID:', id) // Debug log
      const res = await axios.get(`${LOCAL_API}/chats/${id}`)
      console.log('Fetched messages:', res.data) // Debug log
      messages.value = res.data // Ensure messages are properly updated
    } catch (error) {
      console.error('Failed to fetch messages:', error)
      messages.value.push({
        sender: 'System',
        text: 'Error: Could not load previous messages.',
      })
    }
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

    try {
      // Send message to local backend, which handles RAG & LLM processing
      console.log(text.trim())
      const res = await axios.post(`${LOCAL_API}/chats/${chatId.value}`, {
        sender: 'User',
        message: text.trim(),
      })

      // Extract AI response, sources & content
      const aiMessage = {
        sender: 'AI',
        text: res.data.message,
        sources: res.data.sources || [], // File paths
        content: res.data.content || [], // Extracted paragraphs
      }

      // Store AI response locally
      messages.value.push(aiMessage)
    } catch (error) {
      console.error('API Error:', error)

      // Display user-friendly error message in the chat
      messages.value.push({
        sender: 'System',
        text: 'Error: Unable to reach the AI. Please try again later.',
      })
    }
  }

  return { chatId, messages, chatHistory, fetchChatHistory, fetchMessages, sendMessage }
})
