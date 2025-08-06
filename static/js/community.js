let likeClicked = false;
let isBookmarked = false;  // 북마크 상태 저장

function handleLike() {
  if (likeClicked) return;

  const likeCountSpan = document.getElementById('likeCount');
  let count = parseInt(likeCountSpan.innerText);
  likeCountSpan.innerText = count + 1;

  likeClicked = true;
}

function addComment() {
  const input = document.getElementById('commentInput');
  const commentText = input.value.trim();

  if (commentText === '') return;

  const commentList = document.getElementById('commentList');

  const commentCard = document.createElement('div');
  commentCard.className = 'comment-card';

  commentCard.innerHTML = `
    <div class="comment-header">
      <div class="profile-info">
        <div class="profile-icon">익명</div>
        <div class="nickname">익명</div>
      </div>
      <div class="comment-actions">
        <button class="comment-like-btn" onclick="handleCommentLike(this)">👍 <span>0</span></button>
        <button class="delete-btn" onclick="deleteComment(this)">X</button>
      </div>
    </div>

    <div class="comment-body">${commentText}</div>

    <div class="comment-time">방금 전</div>
  `;

  commentList.appendChild(commentCard);
  input.value = '';

  // 댓글 수 업데이트
  const commentCountSpan = document.getElementById('commentCount');
  let currentCount = parseInt(commentCountSpan.innerText);
  commentCountSpan.innerText = currentCount + 1;
}


function handleCommentLike(button) {
  const countSpan = button.querySelector('span');
  let count = parseInt(countSpan.innerText);

  if (!button.classList.contains('liked')) {
    count += 1;
    button.classList.add('liked');
    countSpan.innerText = count;
  }
}

function deleteComment(button) {
  const commentCard = button.closest('.comment-card');
  commentCard.remove();

  const commentCountSpan = document.getElementById('commentCount');
  let currentCount = parseInt(commentCountSpan.innerText);
  commentCountSpan.innerText = currentCount - 1;
}

function handleBookmark(checkbox) {
  const bookmarkImg = document.getElementById('bookmarkImg');

  if (checkbox.checked) {
    bookmarkImg.src = '../images/bookmarks2_checked.png';   // 체크 시 이미지
    isBookmarked = true;                   // 상태 저장
  } else {
    bookmarkImg.src = '../images/bookmarks.png';  // 체크 해제 시 이미지
    isBookmarked = false;                  // 상태 저장
  }

  console.log('북마크 상태:', isBookmarked);
}