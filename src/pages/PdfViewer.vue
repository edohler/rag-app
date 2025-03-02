<template>
  <div class="pdf-container">
    <canvas ref="pdfCanvas"></canvas>
    <!-- <button v-if="foundPage" @click="goToPage(foundPage)" class="jump-button">
      Zum Chunk springen
    </button> -->
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import * as pdfjsLib from 'pdfjs-dist/build/pdf'

// Datei als Worker festlegen (wegen Electron-Sicherheit)
pdfjsLib.GlobalWorkerOptions.workerSrc = '/pdf.worker.min.mjs'

const props = defineProps({
  pdfPath: String, // PDF-Dateipfad
  searchText: String, // Text-Chunk zum Suchen
})

const pdfDoc = ref(null)
const pdfCanvas = ref(null)
const foundPage = ref(null) // Speichert die Seite, wo der Chunk gefunden wurde

// Funktion zum Suchen des Text-Chunks
const searchInPdf = async () => {
  if (!pdfDoc.value || !props.searchText) return

  const words = props.searchText.split(' ').slice(0, 4).join(' ') // Nutze die ersten 4 Wörter

  for (let pageNum = 1; pageNum <= pdfDoc.value.numPages; pageNum++) {
    const page = await pdfDoc.value.getPage(pageNum)
    const textContent = await page.getTextContent()
    const textItems = textContent.items.map((item) => item.str)
    const pageText = textItems.join(' ')

    if (pageText.includes(words)) {
      foundPage.value = pageNum // Speichere die Seite
      goToPage(pageNum)
      break
    }
  }
}

// PDF rendern
const renderPage = async (pageNum) => {
  if (!pdfDoc.value) return

  const page = await pdfDoc.value.getPage(pageNum)
  const viewport = page.getViewport({ scale: 1.5 })
  const canvas = pdfCanvas.value
  const context = canvas.getContext('2d')

  canvas.width = viewport.width
  canvas.height = viewport.height

  const renderContext = { canvasContext: context, viewport }
  await page.render(renderContext)
}

// Springe zu einer bestimmten Seite
const goToPage = async (pageNum) => {
  await renderPage(pageNum)
}

// PDF laden
const loadPdf = async () => {
  if (!props.pdfPath) return
  console.log('Loading PDF:', props.pdfPath)
  pdfDoc.value = await pdfjsLib.getDocument(props.pdfPath).promise

  await renderPage(1) // Starte mit Seite 1
  await searchInPdf() // Suche den Chunk
}

// Aktualisiere, wenn sich die Datei ändert
watch(() => props.pdfPath, loadPdf)

onMounted(loadPdf)
</script>

<style scoped>
.pdf-container {
  position: relative;
  max-width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
}

canvas {
  border: 1px solid #ccc;
}

.jump-button {
  margin-top: 10px;
  padding: 8px 16px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.jump-button:hover {
  background-color: #0056b3;
}
</style>
