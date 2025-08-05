document.addEventListener("DOMContentLoaded", () => {
  const plusBtn = document.getElementById('plusBtn');
  const imagePopup = document.getElementById('imagePopup');
  const chatInput = document.getElementById('chatInput');
  const sendBtn = document.getElementById('sendBtn');
  const chatBox = document.getElementById('chatBox');
  const imageInput = document.getElementById('imageInput');
  const imageSendBtn = document.getElementById('imageSendBtn');

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
