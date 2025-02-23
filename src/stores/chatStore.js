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
        message: 'Error: Could not load previous messages.',
      })
    }
  }

  // Send new message
  const sendMessage = async (message, router) => {
    if (!message.trim()) return

    // If no chat ID, create a new chat
    if (!chatId.value) {
      chatId.value = uuidv4()

      // Optimistically create a new chat entry in chat history
      chatHistory.value.unshift({
        id: chatId.value,
        title: message.split(' ').slice(0, 3).join(' ') || 'Untitled Chat',
      })

      // Navigate immediately to the new chat page
      if (router) {
        router.push(`/chat/${chatId.value}`)
      }
    }

    // Add user's message instantly to the chat
    messages.value.push({ sender: 'User', message })

    try {
      // Send message to local backend, which handles RAG & LLM processing
      // console.log(message.trim())
      const res = await axios.post(`${LOCAL_API}/chats/${chatId.value}`, {
        sender: 'User',
        message: message.trim(),
      })

      // Extract AI response, sources & content
      const aiMessage = {
        sender: 'AI',
        message: res.data.message,
        sources: res.data.sources || [], // File paths
        content: res.data.content || [], // Extracted paragraphs
      }

      // Store AI response locally
      messages.value.push(aiMessage)

      // Fetch updated chat history
      await fetchChatHistory()
    } catch (error) {
      console.error('API Error:', error)

      // Display user-friendly error message in the chat
      messages.value.push({
        sender: 'System',
        message: 'Error: Unable to reach the AI. Please try again later.',
      })
    }
  }

  const deleteChat = async (id) => {
    try {
      await axios.delete(`${LOCAL_API}/chats/${id}`)
      chatHistory.value = chatHistory.value.filter((chat) => chat.id !== id)
      if (chatId.value === id) {
        chatId.value = null
        messages.value = []
      }
    } catch (error) {
      console.error('Failed to delete chat:', error)
    }
  }

  const changeTitle = async (id, newtitle) => {
    try {
      await axios.put(`${LOCAL_API}/chats/${id}/${newtitle}`)
      await fetchChatHistory()

      // If the updated chat is currently open, update the chat title in UI
      if (chatId.value === id) {
        chatHistory.value = chatHistory.value.map((chat) =>
          chat.id === id ? { ...chat, title: newtitle } : chat,
        )
      }
    } catch (error) {
      console.error('Failed to update chat title:', error)
    }
  }

  return {
    chatId,
    messages,
    chatHistory,
    fetchChatHistory,
    fetchMessages,
    sendMessage,
    deleteChat,
    changeTitle,
  }
})
