document.addEventListener("DOMContentLoaded", () => {
  const chatInput = document.querySelector('.chat-input input');
  const sendBtn = document.querySelector('.send-button');
  const chatBox = document.querySelector('.chat-box');
  const plusBtn = document.querySelector('.plus-button');
  const imageInput = document.getElementById('imageInput');
  const imageSendBtn = document.querySelector('.image-send-button');
  const imagePopup = document.getElementById('imagePopup');

  function sendMessage(text) {
    if (!text.trim()) return;

    const message = document.createElement('div');
    message.className = 'message user-message';

    const icon = document.createElement('div');
    icon.className = 'user-icon';
    const content = document.createElement('div');
    content.className = 'message-content';
    content.innerText = text;

    message.appendChild(icon);
    message.appendChild(content);
    chatBox.appendChild(message);
    chatBox.scrollTop = chatBox.scrollHeight;
    chatInput.value = '';

    fetch("/api/messages", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: text }),
    })
      .then((res) => res.json())
      .then((data) => {
        console.log("💬 AI 응답:", data);
        const aiReply = document.createElement('div');
        aiReply.className = 'message ai-message';

        const aiIcon = document.createElement('div');
        aiIcon.className = 'ai-icon';

        const replyContent = document.createElement('div');
        replyContent.className = 'message-content';

        if (data.reply) {
          replyContent.innerText = data.reply;
        } else if (data.error) {
          replyContent.innerText = "❌ 오류: " + data.error;
        } else {
          replyContent.innerText = "⚠️ 알 수 없는 응답입니다.";
        }

        aiReply.appendChild(aiIcon);
        aiReply.appendChild(replyContent);
        
        chatBox.appendChild(aiReply);
        chatBox.scrollTop = chatBox.scrollHeight;
      })
      .catch((error) => {
        console.error("AI 응답 오류:", error);

        const aiReply = document.createElement('div');
        aiReply.className = 'message ai-message';
        const aiIcon = document.createElement('div');
        aiIcon.className = 'ai-icon';
        const replyContent = document.createElement('div');
        replyContent.className = 'message-content';
        replyContent.innerText = "❌ 서버 요청 중 오류가 발생했습니다.";
        aiReply.appendChild(aiIcon);
        aiReply.appendChild(replyContent);
        chatBox.appendChild(aiReply);
        chatBox.scrollTop = chatBox.scrollHeight;
      });
  }

  sendBtn.addEventListener('click', () => {
    sendMessage(chatInput.value);
  });

  chatInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') sendMessage(chatInput.value);
  });

  plusBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    imagePopup.classList.add('show');
  });

  document.addEventListener('click', (e) => {
    if (!imagePopup.contains(e.target) && !plusBtn.contains(e.target)) {
      imagePopup.classList.remove('show');
    }
  });
});
