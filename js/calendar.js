const monthEl = document.getElementById("month");
const yearEl = document.getElementById("year");
const daysGrid = document.getElementById("daysGrid");

let today = new Date();
let currentMonth = today.getMonth();
let currentYear = today.getFullYear();
let selectedDateKey = null;
const scheduleMap = {};

function renderMonthOptions() {
  const monthSelect = document.getElementById("monthSelect");
  monthSelect.innerHTML = "";
  for (let i = 0; i < 12; i++) {
    const opt = document.createElement("option");
    opt.value = i;
    opt.textContent = `${i + 1}월`;
    monthSelect.appendChild(opt);
  }
}

function renderCalendar(year, month) {
  yearEl.innerHTML = `${year}<img src="../images/under_tab.png" class="social-img">`;
  monthEl.innerHTML = `${month + 1}<img src="../images/under_tab.png" class="social-img">`;

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
    const labels = scheduleMap[key]?.map(s => `<div class="label" style="background:${s.color}">${s.title}</div>`).join("") || "";
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
  document.getElementById("overlay").style.display = "block";
  document.getElementById("popup").style.display = "block";

  const yearSelect = document.getElementById("yearSelect");
  yearSelect.innerHTML = "";
  for (let y = 2000; y <= 2030; y++) {
    const opt = document.createElement("option");
    opt.value = y;
    opt.textContent = y + "년";
    if (y === currentYear) opt.selected = true;
    yearSelect.appendChild(opt);
  }

  document.getElementById("monthSelect").value = currentMonth;
}

function closePicker() {
  document.getElementById("overlay").style.display = "none";
  document.getElementById("popup").style.display = "none";
}

function applyPicker() {
  const y = parseInt(document.getElementById("yearSelect").value);
  const m = parseInt(document.getElementById("monthSelect").value);
  currentYear = y;
  currentMonth = m;
  renderCalendar(currentYear, currentMonth);
  closePicker();
}

function openSchedulePopup(dateText) {
  document.getElementById("scheduleOverlay").style.display = "block";
  document.getElementById("schedulePopup").classList.add("active");
  document.getElementById("popupDateText").textContent = dateText;

  const scheduleList = document.getElementById("scheduleList");
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

function closeSchedulePopup() {
  document.getElementById("scheduleOverlay").style.display = "none";
  document.getElementById("schedulePopup").classList.remove("active");
}

document.getElementById("saveScheduleBtn").addEventListener("click", () => {
  const title = document.getElementById("titleInput").value.trim();
  const content = document.getElementById("scheduleInput").value.trim();
  const color = document.getElementById("colorSelect").value;
  const alarmTime = document.getElementById("alarmTime").value;

  if (!selectedDateKey || !title) return;

  if (!scheduleMap[selectedDateKey]) scheduleMap[selectedDateKey] = [];
  scheduleMap[selectedDateKey].push({ title, content, color, alarmTime });

  renderCalendar(currentYear, currentMonth);

  document.getElementById("titleInput").value = "";
  document.getElementById("scheduleInput").value = "";
  document.getElementById("colorSelect").value = "#2196f3";
  document.getElementById("alarmTime").value = "";

  closeSchedulePopup();
});

// 초기 실행
renderMonthOptions();
renderCalendar(currentYear, currentMonth);
