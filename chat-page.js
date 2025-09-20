// chat-page.js
// Minimal chatbot page client. Configure `apiUrl` input and optional `apiKey` token.

function appendMessage(container, text, cls){
  const d = document.createElement('div')
  d.className = 'message ' + cls
  d.textContent = text
  container.appendChild(d)
  container.scrollTop = container.scrollHeight
}

async function sendMessage(apiUrl, apiKey, message){
  // Default contract: POST { message } -> { reply }
  const headers = {'Content-Type':'application/json'}
  if(apiKey) headers['Authorization'] = apiKey
  try{
    const res = await fetch(apiUrl, { method:'POST', headers, body: JSON.stringify({message}) })
    if(!res.ok){
      const txt = await res.text()
      throw new Error(`HTTP ${res.status}: ${txt}`)
    }
    const data = await res.json()
    // Try a few common response shapes
    if(typeof data.reply === 'string') return data.reply
    if(typeof data.response === 'string') return data.response
    if(typeof data.result === 'string') return data.result
    // If it's an object containing text
    if(typeof data === 'object') return JSON.stringify(data)
    return String(data)
  }catch(err){
    return `ERROR: ${err.message}`
  }
}

window.addEventListener('DOMContentLoaded', ()=>{
  const apiUrlEl = document.getElementById('apiUrl')
  const apiKeyEl = document.getElementById('apiKey')
  const messages = document.getElementById('messages')
  const input = document.getElementById('textInput')
  const sendBtn = document.getElementById('sendBtn')

  // Prefill API URL from ?api= query param or default to FastAPI chat endpoint
  const params = new URLSearchParams(window.location.search)
  const defaultApi = params.get('api') || 'http://127.0.0.1:8000/chat'
  apiUrlEl.value = defaultApi

  sendBtn.addEventListener('click', async ()=>{
    const apiUrl = apiUrlEl.value.trim()
    if(!apiUrl) return alert('Please enter the API URL')
    const apiKey = apiKeyEl.value.trim()
    const text = input.value.trim()
    if(!text) return
    appendMessage(messages, text, 'user')
    input.value = ''
    appendMessage(messages, '...', 'bot')
    const reply = await sendMessage(apiUrl, apiKey, text)
    // replace last bot '...' with reply
    const botElems = messages.querySelectorAll('.message.bot')
    const lastBot = botElems[botElems.length-1]
    if(lastBot) lastBot.textContent = reply
    else appendMessage(messages, reply, 'bot')
  })

  input.addEventListener('keydown', (e)=>{ if(e.key === 'Enter') sendBtn.click() })
})
