const monthEl = document.getElementById("month");
const yearEl = document.getElementById("year");
const daysGrid = document.getElementById("daysGrid");

let today = new Date();
let currentMonth = today.getMonth();
let currentYear = today.getFullYear();
let selectedDateKey = null;
const scheduleMap = {};

// 현재 사용자 ID (로그인한 사용자 정보)
let currentUserId = null;

// 🆕 현재 사용자 정보 가져오기
async function getCurrentUser() {
  try {
    const response = await fetch('/api/current-user');
    if (response.ok) {
      const userData = await response.json();
      currentUserId = userData.username;
      console.log('✅ 현재 사용자:', currentUserId);
      return currentUserId;
    } else {
      throw new Error('User not authenticated');
    }
  } catch (error) {
    console.error('❌ 사용자 정보 가져오기 실패:', error);
    // 기본값으로 admin001 사용 (개발용)
    currentUserId = 'admin001';
    return currentUserId;
  }
}

// 🆕 서버에서 일정 데이터 불러오기
async function loadUserSchedules() {
  if (!currentUserId) {
    console.log('❌ 사용자 ID가 없습니다.');
    loadSampleData();
    return;
  }

  try {
    console.log(`📥 사용자 ${currentUserId}의 일정을 불러오는 중...`);
    
    const response = await fetch(`/api/schedules/${currentUserId}`);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const schedules = await response.json();
    console.log('✅ 불러온 일정 데이터:', schedules);
    
    // 🔧 중요: scheduleMap 완전히 초기화
    Object.keys(scheduleMap).forEach(key => delete scheduleMap[key]);
    
    schedules.forEach(schedule => {
      const key = schedule.date; // YYYY-MM-DD 형식
      if (!scheduleMap[key]) scheduleMap[key] = [];
      
      scheduleMap[key].push({
        id: schedule.id,
        title: schedule.title,
        color: schedule.color || '#2196f3',
        alarmTime: schedule.time || '',
        content: schedule.description || ''
      });
    });
    
    // 캘린더 다시 렌더링
    renderCalendar(currentYear, currentMonth);
    console.log('✅ 일정 데이터 로드 완료');
    
  } catch (error) {
    console.error('❌ 일정 로드 실패:', error);
    loadSampleData();
  }
}

// 🔄 샘플 데이터 로드 (서버 연결 실패시 사용)
function loadSampleData() {
  console.log('🔄 샘플 데이터로 대체합니다...');
  
  const sampleSchedules = [
    { date: '2025-08-06', title: '🎨 디자인 작업', color: '#2196f3', time: '09:00' },
    { date: '2025-08-07', title: '🤝 클라이언트 미팅', color: '#4caf50', time: '14:00' },
    { date: '2025-08-08', title: '📚 스터디 모임', color: '#ff9800', time: '10:30' },
    { date: '2025-08-09', title: '🍗 친구들과 치킨', color: '#f44336', time: '19:00' },
    { date: '2025-08-10', title: '💪 헬스장 운동', color: '#9c27b0', time: '07:00' }
  ];
  
  // scheduleMap 초기화
  Object.keys(scheduleMap).forEach(key => delete scheduleMap[key]);
  
  sampleSchedules.forEach(schedule => {
    const key = schedule.date;
    if (!scheduleMap[key]) scheduleMap[key] = [];
    
    scheduleMap[key].push({
      title: schedule.title,
      color: schedule.color,
      alarmTime: schedule.time,
      content: ''
    });
  });
  
  renderCalendar(currentYear, currentMonth);
  console.log('✅ 샘플 데이터 로드 완료');
}

// 🆕 서버에 일정 저장
async function saveScheduleToServer(scheduleData) {
  try {
    const response = await fetch('/api/schedules', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
      },
      credentials: 'same-origin', // 쿠키 포함
      body: JSON.stringify({
        date: selectedDateKey,
        title: scheduleData.title,
        time: scheduleData.alarmTime,
        color: scheduleData.color,
        description: scheduleData.content
      })
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
    }
    
    const result = await response.json();
    console.log('✅ 서버에 일정 저장 완료:', result);
    
    // 🔧 중요: 저장 성공 후 서버에서 최신 데이터 다시 불러오기
    await loadUserSchedules();
    
    // 성공 알림
    showNotification('일정이 저장되었습니다!', 'success');
    return result;
    
  } catch (error) {
    console.error('❌ 서버 저장 실패:', error);
    showNotification(`저장 실패: ${error.message}`, 'error');
    throw error;
  }
}

// 🆕 알림 표시 함수
function showNotification(message, type = 'info') {
  // 간단한 알림 (나중에 더 예쁘게 만들 수 있음)
  if (type === 'success') {
    console.log('✅ ' + message);
  } else if (type === 'error') {
    console.error('❌ ' + message);
  } else {
    console.log('ℹ️ ' + message);
  }
  
  // 선택사항: alert 대신 토스트 알림으로 교체 가능
  // alert(message);
}

function renderMonthOptions() {
  const monthSelect = document.getElementById("monthSelect");
  if (monthSelect) {
    monthSelect.innerHTML = "";
    for (let i = 0; i < 12; i++) {
      const opt = document.createElement("option");
      opt.value = i;
      opt.textContent = `${i + 1}월`;
      monthSelect.appendChild(opt);
    }
  }
}

function renderCalendar(year, month) {
  if (yearEl) yearEl.textContent = year;
  if (monthEl) monthEl.textContent = month + 1;

  if (!daysGrid) return;

  const firstDay = new Date(year, month, 1).getDay();
  const lastDate = new Date(year, month + 1, 0).getDate();
  const prevLastDate = new Date(year, month, 0).getDate();

  let html = "";

  // 이전 달 날짜들
  for (let i = firstDay - 1; i >= 0; i--) {
    html += `<div class="day inactive">${prevLastDate - i}</div>`;
  }

  // 현재 달 날짜들
  for (let i = 1; i <= lastDate; i++) {
    const isToday = year === today.getFullYear() && month === today.getMonth() && i === today.getDate();
    const key = `${year}-${String(month + 1).padStart(2, '0')}-${String(i).padStart(2, '0')}`;
    
    // 🆕 툴팁을 위한 title 속성 추가
    const labels = scheduleMap[key]?.map(s => 
      `<div class="label" title="${s.title}" style="background:${s.color}">${s.title}</div>`
    ).join("") || "";
    
    html += `<div class="day ${isToday ? "today" : ""}" data-date="${key}">${i}<div class="label-container">${labels}</div></div>`;
  }

  // 다음 달 날짜들
  const totalCells = firstDay + lastDate;
  const nextEmpty = 7 - (totalCells % 7);
  if (nextEmpty < 7) {
    for (let i = 1; i <= nextEmpty; i++) {
      html += `<div class="day inactive">${i}</div>`;
    }
  }

  daysGrid.innerHTML = html;

  // 날짜 클릭 이벤트 추가
  document.querySelectorAll(".day").forEach(day => {
    day.addEventListener("click", () => {
      if (!day.classList.contains("inactive")) {
        document.querySelectorAll(".day.selected").forEach(el => el.classList.remove("selected"));
        day.classList.add("selected");
        const dayNum = parseInt(day.textContent.trim());
        const dateStr = `${currentMonth + 1}월 ${dayNum}일`;
        selectedDateKey = `${currentYear}-${String(currentMonth + 1).padStart(2, '0')}-${String(dayNum).padStart(2, '0')}`;
        openSchedulePopup(dateStr);
      }
    });
  });
}

function changeMonth(delta) {
  currentMonth += delta;
  if (currentMonth > 11) {
    currentMonth = 0;
    currentYear++;
  } else if (currentMonth < 0) {
    currentMonth = 11;
    currentYear--;
  }
  renderCalendar(currentYear, currentMonth);
}

function openPicker() {
  const overlay = document.getElementById("overlay");
  const popup = document.getElementById("popup");
  
  if (overlay) overlay.style.display = "block";
  if (popup) popup.style.display = "block";

  const yearSelect = document.getElementById("yearSelect");
  if (yearSelect) {
    yearSelect.innerHTML = "";
    for (let y = 2000; y <= 2030; y++) {
      const opt = document.createElement("option");
      opt.value = y;
      opt.textContent = y + "년";
      if (y === currentYear) opt.selected = true;
      yearSelect.appendChild(opt);
    }
  }

  const monthSelect = document.getElementById("monthSelect");
  if (monthSelect) {
    monthSelect.value = currentMonth;
  }
}

function closePicker() {
  const overlay = document.getElementById("overlay");
  const popup = document.getElementById("popup");
  
  if (overlay) overlay.style.display = "none";
  if (popup) popup.style.display = "none";
}

function applyPicker() {
  const yearSelect = document.getElementById("yearSelect");
  const monthSelect = document.getElementById("monthSelect");
  
  if (yearSelect && monthSelect) {
    const y = parseInt(yearSelect.value);
    const m = parseInt(monthSelect.value);
    currentYear = y;
    currentMonth = m;
    renderCalendar(currentYear, currentMonth);
  }
  closePicker();
}

function openSchedulePopup(dateText) {
  const scheduleOverlay = document.getElementById("scheduleOverlay");
  const schedulePopup = document.getElementById("schedulePopup");
  const popupDateText = document.getElementById("popupDateText");
  
  if (scheduleOverlay) scheduleOverlay.style.display = "block";
  if (schedulePopup) schedulePopup.classList.add("active");
  if (popupDateText) popupDateText.textContent = dateText;

  const scheduleList = document.getElementById("scheduleList");
  if (scheduleList) {
    scheduleList.innerHTML = "";

    if (scheduleMap[selectedDateKey] && scheduleMap[selectedDateKey].length > 0) {
      scheduleMap[selectedDateKey].forEach(sch => {
        const li = document.createElement("li");

        const leftDiv = document.createElement("div");
        leftDiv.className = "schedule-left";

        const colorDot = document.createElement("div");
        colorDot.className = "schedule-color-dot";
        colorDot.style.backgroundColor = sch.color;

        const titleSpan = document.createElement("span");
        titleSpan.textContent = sch.title;

        leftDiv.appendChild(colorDot);
        leftDiv.appendChild(titleSpan);

        const alarmSpan = document.createElement("span");
        alarmSpan.className = "schedule-alarm";
        alarmSpan.textContent = sch.alarmTime ? `⏰ ${sch.alarmTime}` : "";

        li.appendChild(leftDiv);
        li.appendChild(alarmSpan);
        scheduleList.appendChild(li);
      });
    } else {
      const li = document.createElement("li");
      li.textContent = "등록된 일정이 없습니다.";
      li.style.color = "#999";
      li.style.fontStyle = "italic";
      scheduleList.appendChild(li);
    }
  }
}

function closeSchedulePopup() {
  const scheduleOverlay = document.getElementById("scheduleOverlay");
  const schedulePopup = document.getElementById("schedulePopup");
  
  if (scheduleOverlay) scheduleOverlay.style.display = "none";
  if (schedulePopup) schedulePopup.classList.remove("active");
}

// 🆕 입력 필드 초기화 함수
function clearInputFields() {
  const titleInput = document.getElementById("titleInput");
  const scheduleInput = document.getElementById("scheduleInput");
  const colorSelect = document.getElementById("colorSelect");
  const alarmTime = document.getElementById("alarmTime");

  if (titleInput) titleInput.value = "";
  if (scheduleInput) scheduleInput.value = "";
  if (colorSelect) colorSelect.value = "#2196f3";
  if (alarmTime) alarmTime.value = "";
}

// 🆕 입력 유효성 검사
function validateScheduleInput(title, selectedDateKey) {
  if (!selectedDateKey) {
    showNotification('날짜를 선택해주세요.', 'error');
    return false;
  }
  
  if (!title || title.trim().length === 0) {
    showNotification('일정 제목을 입력해주세요.', 'error');
    return false;
  }
  
  if (title.trim().length > 100) {
    showNotification('제목이 너무 깁니다. (최대 100자)', 'error');
    return false;
  }
  
  return true;
}

// 🆕 삼지창 메뉴 이벤트 설정 함수
function setupMenuEvents() {
  console.log('🔗 삼지창 메뉴 이벤트 설정 중...');
  
  // 다양한 방법으로 메뉴 요소들 찾기
  const menuElements = document.querySelectorAll('*');
  
  menuElements.forEach(element => {
    const text = element.textContent?.trim() || '';
    
    // AI CHAT 버튼 찾기
    if (text === 'AI CHAT' || text.includes('AI CHAT')) {
      element.style.cursor = 'pointer';
      element.addEventListener('click', function(e) {
        e.preventDefault();
        console.log('🤖 AI CHAT 클릭');
        window.location.href = '/chat';
      });
      console.log('✅ AI CHAT 버튼 이벤트 등록 완료');
    }
    
    // COMMUNITY 버튼 찾기
    if (text === 'community' || text === 'Community' || text === 'COMMUNITY') {
      element.removeAttribute('onclick'); // 기존 onclick 제거
      element.style.cursor = 'pointer';
      element.addEventListener('click', function(e) {
        e.preventDefault();
        e.stopPropagation();
        console.log('🏘️ COMMUNITY 클릭');
        window.location.href = '/community';
      });
      console.log('✅ COMMUNITY 버튼 이벤트 등록 완료');
    }
    
    // NEW CALENDAR 버튼 찾기
    if (text === 'new calendar' || text.includes('new calendar') || text === 'New') {
      element.style.cursor = 'pointer';
      element.addEventListener('click', function(e) {
        e.preventDefault();
        console.log('📅 NEW CALENDAR 클릭');
        window.location.reload();
      });
      console.log('✅ NEW CALENDAR 버튼 이벤트 등록 완료');
    }
  });
}

// 🆕 DOMContentLoaded 이벤트 - 초기화 및 이벤트 등록
document.addEventListener('DOMContentLoaded', async function() {
  console.log('📅 캘린더 초기화 시작...');
  
  try {
    // 1. 현재 사용자 정보 가져오기
    await getCurrentUser();
    
    // 2. 월 선택 옵션 렌더링
    renderMonthOptions();
    
    // 3. 사용자 일정 불러오기
    await loadUserSchedules();
    
    // 4. 저장 버튼 이벤트 등록
    const saveBtn = document.getElementById("saveScheduleBtn");
    if (saveBtn) {
      saveBtn.addEventListener("click", async () => {
        const titleInput = document.getElementById("titleInput");
        const scheduleInput = document.getElementById("scheduleInput");
        const colorSelect = document.getElementById("colorSelect");
        const alarmTime = document.getElementById("alarmTime");

        const title = titleInput ? titleInput.value.trim() : "";
        const content = scheduleInput ? scheduleInput.value.trim() : "";
        const color = colorSelect ? colorSelect.value : "#2196f3";
        const alarm = alarmTime ? alarmTime.value : "";

        // 입력 유효성 검사
        if (!validateScheduleInput(title, selectedDateKey)) {
          return;
        }

        const scheduleData = { title, content, color, alarmTime: alarm };

        try {
          // 🔧 중요: 서버 저장 (이미 loadUserSchedules() 호출됨)
          await saveScheduleToServer(scheduleData);
          
          // 입력 필드 초기화
          clearInputFields();
          
          // 팝업 닫기
          closeSchedulePopup();
          
        } catch (error) {
          // 서버 저장 실패시에도 로컬에는 저장 (오프라인 모드)
          console.log('📱 서버 저장 실패, 로컬에만 저장합니다.');
          
          if (!scheduleMap[selectedDateKey]) scheduleMap[selectedDateKey] = [];
          scheduleMap[selectedDateKey].push(scheduleData);

          renderCalendar(currentYear, currentMonth);
          clearInputFields();
          closeSchedulePopup();
        }
      });
    }
    
    // 🆕 5. 삼지창 메뉴 이벤트 등록 (지연 실행으로 DOM 완전 로드 보장)
    setTimeout(setupMenuEvents, 2000);
    
    console.log('✅ 캘린더 초기화 완료');
    
  } catch (error) {
    console.error('❌ 캘린더 초기화 실패:', error);
    // 초기화 실패시에도 기본 기능은 작동하도록
    renderMonthOptions();
    renderCalendar(currentYear, currentMonth);
    // 메뉴 이벤트는 항상 등록
    setTimeout(setupMenuEvents, 2000);
  }
});