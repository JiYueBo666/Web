<script setup>
import { ref, nextTick, computed } from 'vue'

const messages = ref([])
const isWaitingResponse = ref(false)
const currentSessionId = ref(1)
const chatHistory = ref([])
const currentScene = ref('math')

// 发送消息到服务器
const sendMessageToServer = async (message) => {
  try {
    console.log('Sending message:', message)
    const response = await fetch('http://localhost:8000/chat/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        role: 'user',
        content: message,
        stream: true,
        is_json: false,
        history: chatHistory.value,
        scene: currentScene.value
      })
    })
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }
    
    return response
  } catch (error) {
    console.error('发送消息失败:', error)
    throw error
  }
}

// 处理服务器响应
const handleServerResponse = async (response) => {
  const reader = response.body.getReader()
  const decoder = new TextDecoder()
  
  const aiMessage = {
    text: '',
    isSelf: false,
    time: new Date().toLocaleTimeString(),
    sessionId: currentSessionId.value
  }
  messages.value.push(aiMessage)
  
  let fullResponse = ''

  try {
    while (true) {
      const { value, done } = await reader.read()
      if (done) break
      
      const chunk = decoder.decode(value)
      const lines = chunk.split('\n')
      
      for (const line of lines) {
        if (line.startsWith('data: ')) {
          const data = line.slice(6).trim()
          if (data === '[DONE]' || !data) continue
          try {
            console.log('Received chunk:', data)
            messages.value = [...messages.value.slice(0, -1), {
              ...aiMessage,
              text: aiMessage.text + data
            }]
            aiMessage.text += data
            fullResponse += data
            
            await nextTick()
            
            const chatArea = document.querySelector('.message-container')
            if (chatArea) {
              chatArea.scrollTop = chatArea.scrollHeight
            }
          } catch (e) {
            console.error('解析消息失败:', e)
          }
        }
      }
    }
    
    chatHistory.value.push({
      role: 'assistant',
      content: fullResponse
    })
    
  } catch (error) {
    console.error('读取响应流失败:', error)
    aiMessage.text = '抱歉，接收消息时发生错误'
  } finally {
    isWaitingResponse.value = false
  }
}

// 添加用户消息
const addUserMessage = (text) => {
  // 添加用户消息到显示列表
  messages.value.push({
    text,
    isSelf: true,
    time: new Date().toLocaleTimeString(),
    sessionId: currentSessionId.value
  })
  
  // 添加用户消息到历史记录
  chatHistory.value.push({
    role: 'user',
    content: text
  })
}

// 发送消息的主函数
const send = async () => {
  const inputElement = document.getElementById('input')
  const inputText = inputElement.value.trim()
  
  if (!inputText || isWaitingResponse.value) return
  
  try {
    isWaitingResponse.value = true
    addUserMessage(inputText)
    inputElement.value = ''
    const response = await sendMessageToServer(inputText)
    await handleServerResponse(response)
  } catch (error) {
    messages.value.push({
      text: '发送消息失败，请稍后重试',
      isSelf: false,
      time: new Date().toLocaleTimeString(),
      sessionId: currentSessionId.value
    })
  } finally {
    isWaitingResponse.value = false
  }
}

// 清除聊天记录并开始新会话
const startNewSession = () => {
  messages.value = []
  chatHistory.value = [] // 清空历史对话
  currentSessionId.value++
}

// 添加场景切换处理函数
const handleSceneChange = (event) => {
  currentScene.value = event.target.value === 'value1' ? 'math' : 'eng'
}
</script>

<template>
  <div id="container">
    <form id="sideBar">
      <div class="radio-option">
        <input 
          type="radio" 
          id="mathOption" 
          name="options" 
          value="value1" 
          checked
          @change="handleSceneChange"
        >
        <label for="mathOption">数学</label>
      </div>
      <div class="radio-option">
        <input 
          type="radio" 
          id="englishOption" 
          name="options" 
          value="value2"
          @change="handleSceneChange"
        >
        <label for="englishOption">英语</label>
      </div>
      <button id = "setting">&#8617; 设置</button>
    </form>
    <div id="rightBar">
      <div id="chatArea">
        <div class="message-container">
          <div v-for="(msg, index) in messages" 
               :key="index" 
               :class="['message', msg.isSelf ? 'self' : 'other']">
            <div class="message-content">
              <!-- 使用计算属性显示消息内容 -->
              {{ typeof msg.text === 'function' ? msg.text() : msg.text }}
            </div>
            <div class="message-time">{{ msg.time }}</div>
          </div>
        </div>
      </div>
      <div class="inputPanel">
        <textarea 
          type="text" 
          id="input" 
          placeholder="请输入你的问题"
          :disabled="isWaitingResponse"
        ></textarea>
        <button 
          type="button" 
          id="sendIt" 
          @click="send"
          :disabled="isWaitingResponse"
        >
          {{ isWaitingResponse ? '等待回复...' : '发送' }}
        </button>
      </div>
    </div>
  </div>
</template>

<style scoped>
#rightBar {
  background-color: rgb(240, 233, 233);
  width: 85%;
  height: 100%;
  position: fixed;
  top: 0;
  left: 15%;
}

#sideBar {
  border-right: none;
  position: fixed;
  top: 0;
  left: 0;
  width: 15%;
  height: 100%;
  background-image: linear-gradient(to bottom,
      transparent,
      transparent 10%,
      gray 20%,
      gray 90%,
      transparent 100%,
      transparent);
  background-position: right;
  background-size: 1px 100%;
  background-repeat: no-repeat;
  display: flex;
  flex-direction: column;
}
#sideBar >label,#sideBar>input{
  margin-bottom: 8px; /* 可选：添加一些间距 */
}

#setting{
  border-radius: 50%;
  background-color: #cbe2fc;
  position: absolute;
  bottom: 0;
  width: 95px;
  height: 95px;
  left: 50%;
  transform: translate(-50%, 0);
}

#chatArea {
  background-color: white;
  border-radius: 10px 10px 0 0;
  position: fixed;
  top: 20px;
  left: 25%;
  right: 15%;
  width: 60%;
  height: 70%;
  overflow: hidden;
}

.inputPanel {
  background-color: rgb(236, 234, 234);
  border-radius: 10px;
  position: relative;
  top: 75%;
  left: 11.5%;
  width: 71%;
  height: 20%;
  border: 2px solid rgb(221, 221, 221);
}

#sendIt {
  position: absolute;
  bottom: 2px;
  right: 2px;
  width: 80px;
  border-radius: 30px;
  color: white;
  background-color: rgb(189, 227, 245);
}

#input {
  position: absolute;
  bottom: 0px;
  left: 0px;
  width: 100%;
  height: 99%;
  border: none;
  border-radius: 10px;
  padding: 10px;
  font-family: "微软雅黑", Arial, sans-serif;
  font-size: 20px;
  display: block;
  padding: 5px;
  line-height: normal;
  align-items: flex-start;
  text-align: left;
  text-indent: 10px;
}

/* 添加新的消息样式 */
.message-container {
  padding: 20px;
  height: 100%;
  overflow-y: auto;
  scroll-behavior: smooth; /* 添加平滑滚动效果 */
}

.message {
  margin: 10px 0;
  max-width: 70%;
  clear: both;
}

.message-content {
  padding: 10px;
  border-radius: 10px;
  word-wrap: break-word;
  white-space: pre-wrap; /* 保留换行和空格 */
  text-align: left;
}

.message-time {
  font-size: 12px;
  color: #999;
  margin-top: 5px;
}

.self {
  float: right;
}

.self .message-content {
  background-color: #95ec69;
}

.other {
  float: left;
}

.other .message-content {
  background-color: white;
  border: 1px solid #e5e5e5;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

textarea:disabled {
  background-color: #f5f5f5;
  cursor: not-allowed;
}

.radio-option {
  padding: 10px;
  margin: 5px;
  background-color: #f0f0f0;  /* 默认背景色 */
  border-radius: 5px;
  cursor: pointer;
}

/* 当radio被选中时，改变对应容器的背景色 */
.radio-option input[type="radio"]:checked + label {
  color: #fff;
  font-weight: bold;
}

.radio-option:has(input[type="radio"]:checked) {
  background-color: #cbe2fc;  /* 选中时的背景色 */
}

/* 鼠标悬停效果 */
.radio-option:hover {
  background-color: #e0e0e0;
}

.radio-option:has(input[type="radio"]:checked):hover {
  background-color: #85dc59;
}

/* 让label和radio更好看 */
.radio-option label {
  margin-left: 5px;
  cursor: pointer;
}

.radio-option input[type="radio"] {
  cursor: pointer;
}

.session-id {
  font-size: 12px;
  color: #666;
  margin-bottom: 5px;
}
</style>
