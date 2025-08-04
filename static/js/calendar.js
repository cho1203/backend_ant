// const monthEl = document.getElementById("month");
// const yearEl = document.getElementById("year");
// const daysGrid = document.getElementById("daysGrid");

// let today = new Date();
// let currentMonth = today.getMonth();
// let currentYear = today.getFullYear();
// let selectedDateKey = null;
// const scheduleMap = {};

// function renderMonthOptions() {
//   const monthSelect = document.getElementById("monthSelect");
//   monthSelect.innerHTML = "";
//   for (let i = 0; i < 12; i++) {
//     const opt = document.createElement("option");
//     opt.value = i;
//     opt.textContent = `${i + 1}월`;
//     monthSelect.appendChild(opt);
//   }
// }

// function renderCalendar(year, month) {
//   yearEl.textContent = year;
//   monthEl.textContent = month + 1;

//   const firstDay = new Date(year, month, 1).getDay();
//   const lastDate = new Date(year, month + 1, 0).getDate();
//   const prevLastDate = new Date(year, month, 0).getDate();

//   let html = "";

//   for (let i = firstDay - 1; i >= 0; i--) {
//     html += `<div class="day inactive">${prevLastDate - i}</div>`;
//   }

//   for (let i = 1; i <= lastDate; i++) {
//     const isToday = year === today.getFullYear() && month === today.getMonth() && i === today.getDate();
//     const key = `${year}-${String(month + 1).padStart(2, '0')}-${String(i).padStart(2, '0')}`;
//     const labels = scheduleMap[key]?.map(s => `<div class="label" style="background:${s.color}">${s.title}</div>`).join("") || "";
//     html += `<div class="day ${isToday ? "today" : ""}" data-date="${key}">${i}<div class="label-container">${labels}</div></div>`;
//   }

//   const totalCells = firstDay + lastDate;
//   const nextEmpty = 7 - (totalCells % 7);
//   if (nextEmpty < 7) {
//     for (let i = 1; i <= nextEmpty; i++) {
//       html += `<div class="day inactive">${i}</div>`;
//     }
//   }

//   daysGrid.innerHTML = html;

//   document.querySelectorAll(".day").forEach(day => {
//     day.addEventListener("click", () => {
//       if (!day.classList.contains("inactive")) {
//         document.querySelectorAll(".day.selected").forEach(el => el.classList.remove("selected"));
//         day.classList.add("selected");
//         const dayNum = parseInt(day.textContent.trim());
//         const dateStr = `${currentMonth + 1}월 ${dayNum}일`;
//         selectedDateKey = `${currentYear}-${String(currentMonth + 1).padStart(2, '0')}-${String(dayNum).padStart(2, '0')}`;
//         openSchedulePopup(dateStr);
//       }
//     });
//   });
// }

// function changeMonth(delta) {
//   currentMonth += delta;
//   if (currentMonth > 11) {
//     currentMonth = 0;
//     currentYear++;
//   } else if (currentMonth < 0) {
//     currentMonth = 11;
//     currentYear--;
//   }
//   renderCalendar(currentYear, currentMonth);
// }

// function openPicker() {
//   document.getElementById("overlay").style.display = "block";
//   document.getElementById("popup").style.display = "block";

//   const yearSelect = document.getElementById("yearSelect");
//   yearSelect.innerHTML = "";
//   for (let y = 2000; y <= 2030; y++) {
//     const opt = document.createElement("option");
//     opt.value = y;
//     opt.textContent = y + "년";
//     if (y === currentYear) opt.selected = true;
//     yearSelect.appendChild(opt);
//   }

//   document.getElementById("monthSelect").value = currentMonth;
// }

// function closePicker() {
//   document.getElementById("overlay").style.display = "none";
//   document.getElementById("popup").style.display = "none";
// }

// function applyPicker() {
//   const y = parseInt(document.getElementById("yearSelect").value);
//   const m = parseInt(document.getElementById("monthSelect").value);
//   currentYear = y;
//   currentMonth = m;
//   renderCalendar(currentYear, currentMonth);
//   closePicker();
// }

// function openSchedulePopup(dateText) {
//   document.getElementById("scheduleOverlay").style.display = "block";
//   document.getElementById("schedulePopup").classList.add("active");
//   document.getElementById("popupDateText").textContent = dateText;

//   const scheduleList = document.getElementById("scheduleList");
//   scheduleList.innerHTML = "";

//   if (scheduleMap[selectedDateKey]) {
//     scheduleMap[selectedDateKey].forEach(sch => {
//       const li = document.createElement("li");

//       const leftDiv = document.createElement("div");
//       leftDiv.className = "schedule-left";

//       const colorDot = document.createElement("div");
//       colorDot.className = "schedule-color-dot";
//       colorDot.style.backgroundColor = sch.color;

//       const titleSpan = document.createElement("span");
//       titleSpan.textContent = sch.title;

//       leftDiv.appendChild(colorDot);
//       leftDiv.appendChild(titleSpan);

//       const alarmSpan = document.createElement("span");
//       alarmSpan.className = "schedule-alarm";
//       alarmSpan.textContent = sch.alarmTime ? `⏰ ${sch.alarmTime}` : "";

//       li.appendChild(leftDiv);
//       li.appendChild(alarmSpan);
//       scheduleList.appendChild(li);
//     });
//   } else {
//     const li = document.createElement("li");
//     li.textContent = "등록된 일정이 없습니다.";
//     scheduleList.appendChild(li);
//   }
// }

// function closeSchedulePopup() {
//   document.getElementById("scheduleOverlay").style.display = "none";
//   document.getElementById("schedulePopup").classList.remove("active");
// }

// document.getElementById("saveScheduleBtn").addEventListener("click", () => {
//   const title = document.getElementById("titleInput").value.trim();
//   const content = document.getElementById("scheduleInput").value.trim();
//   const color = document.getElementById("colorSelect").value;
//   const alarmTime = document.getElementById("alarmTime").value;

//   if (!selectedDateKey || !title) return;

//   if (!scheduleMap[selectedDateKey]) scheduleMap[selectedDateKey] = [];
//   scheduleMap[selectedDateKey].push({ title, content, color, alarmTime });

//   renderCalendar(currentYear, currentMonth);

//   document.getElementById("titleInput").value = "";
//   document.getElementById("scheduleInput").value = "";
//   document.getElementById("colorSelect").value = "#2196f3";
//   document.getElementById("alarmTime").value = "";

//   closeSchedulePopup();
// });

// // 초기 실행
// renderMonthOptions();
// renderCalendar(currentYear, currentMonth);

const monthEl = document.getElementById("month");
const yearEl = document.getElementById("year");
const daysGrid = document.getElementById("daysGrid");

let today = new Date();
let currentMonth = today.getMonth();
let currentYear = today.getFullYear();
let selectedDateKey = null;
const scheduleMap = {};

// 사용자 ID (실제로는 로그인한 사용자 정보에서 가져와야 함)
const currentUserId = 'admin001'; // 또는 서버에서 전달받은 사용자 ID

// 🆕 서버에서 일정 데이터 불러오기
async function loadUserSchedules(userId) {
  try {
    console.log(`📥 사용자 ${userId}의 일정을 불러오는 중...`);
    
    const response = await fetch(`/api/schedules/${userId}`);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const schedules = await response.json();
    console.log('✅ 불러온 일정 데이터:', schedules);
    
    // scheduleMap 초기화 후 데이터 추가
    Object.keys(scheduleMap).forEach(key => delete scheduleMap[key]);
    
    schedules.forEach(schedule => {
      const key = schedule.date; // YYYY-MM-DD 형식
      if (!scheduleMap[key]) scheduleMap[key] = [];
      
      scheduleMap[key].push({
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
    
    // 🔄 실패시 샘플 데이터로 대체 (개발용)
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
      },
      body: JSON.stringify({
        user_id: currentUserId,
        date: selectedDateKey,
        title: scheduleData.title,
        time: scheduleData.alarmTime,
        color: scheduleData.color,
        description: scheduleData.content
      })
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const result = await response.json();
    console.log('✅ 서버에 일정 저장 완료:', result);
    
  } catch (error) {
    console.error('❌ 서버 저장 실패:', error);
    console.log('📱 로컬에만 저장됩니다.');
  }
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

  for (let i = firstDay - 1; i >= 0; i--) {
    html += `<div class="day inactive">${prevLastDate - i}</div>`;
  }

  for (let i = 1; i <= lastDate; i++) {
    const isToday = year === today.getFullYear() && month === today.getMonth() && i === today.getDate();
    const key = `${year}-${String(month + 1).padStart(2, '0')}-${String(i).padStart(2, '0')}`;
    const labels = scheduleMap[key]?.map(s => `<div class="label" title="${s.title}" style="background:${s.color}">${s.title}</div>`).join("") || "";
    html += `<div class="day ${isToday ? "today" : ""}" data-date="${key}">${i}<div class="label-container">${labels}</div></div>`;
  }

  const totalCells = firstDay + lastDate;
  const nextEmpty = 7 - (totalCells % 7);
  if (nextEmpty < 7) {
    for (let i = 1; i <= nextEmpty; i++) {
      html += `<div class="day inactive">${i}</div>`;
    }
  }

  daysGrid.innerHTML = html;

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

    if (scheduleMap[selectedDateKey]) {
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

// 🆕 수정된 저장 버튼 이벤트 (서버 저장 포함)
document.addEventListener('DOMContentLoaded', function() {
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

      if (!selectedDateKey || !title) return;

      const scheduleData = { title, content, color, alarmTime: alarm };

      // 로컬에 저장
      if (!scheduleMap[selectedDateKey]) scheduleMap[selectedDateKey] = [];
      scheduleMap[selectedDateKey].push(scheduleData);

      // 서버에 저장 시도
      await saveScheduleToServer(scheduleData);

      renderCalendar(currentYear, currentMonth);

      // 입력 필드 초기화
      if (titleInput) titleInput.value = "";
      if (scheduleInput) scheduleInput.value = "";
      if (colorSelect) colorSelect.value = "#2196f3";
      if (alarmTime) alarmTime.value = "";

      closeSchedulePopup();
    });
  }

  // 🆕 페이지 로드시 사용자 일정 불러오기
  console.log('📅 캘린더 초기화 중...');
  renderMonthOptions();
  loadUserSchedules(currentUserId); // 서버에서 데이터 불러오기
});