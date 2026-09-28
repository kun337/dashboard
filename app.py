<!DOCTYPE html>
<html lang="ko" class="h-full">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>실시간 현황 대시보드 (Real-time Analytics Dashboard)</title>
  
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Chart.js CDN -->
  <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.7/dist/chart.umd.min.js"></script>
  <!-- FontAwesome CDN -->
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" />
  <!-- Google Fonts: Inter & Noto Sans KR -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap" rel="stylesheet">

  <script>
    tailwind.config = {
      darkMode: 'class',
      theme: {
        extend: {
          fontFamily: {
            sans: ['Inter', 'Noto Sans KR', 'sans-serif'],
          },
          colors: {
            brand: {
              50: '#f0f5ff',
              100: '#e0ebff',
              500: '#3b82f6',
              600: '#2563eb',
              700: '#1d4ed8',
              900: '#1e3a8a',
            }
          }
        }
      }
    }
  </script>

  <style>
    /* Custom Scrollbar Styling */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: rgba(156, 163, 175, 0.4); border-radius: 9999px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(107, 114, 128, 0.7); }
    
    .glass-panel {
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
    }
  </style>
</head>
<body class="bg-slate-50 dark:bg-slate-950 text-slate-800 dark:text-slate-100 min-h-full font-sans transition-colors duration-200 antialiased selection:bg-brand-500 selection:text-white">

  <div id="app" class="min-h-screen flex flex-col">
    
    <!-- Top Header -->
    <header class="sticky top-0 z-30 bg-white/80 dark:bg-slate-900/80 backdrop-blur-md border-b border-slate-200 dark:border-slate-800 px-4 lg:px-8 py-3 transition-colors">
      <div class="max-w-[1600px] mx-auto flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        
        <!-- Brand Title & Tagline -->
        <div class="flex items-center gap-3">
          <div class="p-2.5 bg-brand-600 text-white rounded-xl shadow-lg shadow-brand-500/30 flex items-center justify-center">
            <i class="fa-solid fa-chart-line text-xl"></i>
          </div>
          <div>
            <div class="flex items-center gap-2">
              <h1 class="font-extrabold text-xl tracking-tight text-slate-900 dark:text-white">실시간 현황 대시보드</h1>
              <span id="livePulseBadge" class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800 dark:bg-emerald-950/80 dark:text-emerald-400 border border-emerald-300/50 dark:border-emerald-800">
                <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
                <span id="statusText">정상 연동</span>
              </span>
            </div>
            <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5 flex items-center gap-2">
              <span>Google Sheets CSV &amp; 데이터 오토 파싱</span>
              <span class="text-slate-300 dark:text-slate-700">•</span>
              <span id="dataTimeText">최근 수신: -</span>
            </p>
          </div>
        </div>

        <!-- Controls & Status Badge -->
        <div class="flex flex-wrap items-center gap-2 sm:gap-3">
          <!-- Refresh Timer Badge -->
          <div class="flex items-center gap-2 px-3 py-1.5 bg-slate-100 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700/80 rounded-lg text-xs font-medium text-slate-600 dark:text-slate-300">
            <i class="fa-regular fa-clock text-brand-500"></i>
            <span>갱신: <b id="countdown" class="text-slate-900 dark:text-white font-bold">30</b>초</span>
            <button id="pauseBtn" title="자동 갱신 일시정지/재개" class="hover:text-brand-600 dark:hover:text-brand-400 ml-1">
              <i id="pauseIcon" class="fa-solid fa-pause"></i>
            </button>
          </div>

          <!-- Manual Refresh Button -->
          <button id="refreshBtn" class="inline-flex items-center gap-1.5 px-3.5 py-1.5 bg-brand-600 hover:bg-brand-700 text-white rounded-lg text-xs font-semibold shadow-md shadow-brand-500/20 active:scale-95 transition">
            <i id="refreshSpinner" class="fa-solid fa-rotate"></i>
            <span>지금 새로고침</span>
          </button>

          <!-- Source Settings Modal Button -->
          <button id="openSettingsBtn" class="p-2 text-slate-600 dark:text-slate-300 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 rounded-lg transition" title="데이터 소스 설정">
            <i class="fa-solid fa-gear"></i>
          </button>

          <!-- Dark/Light Theme Toggle -->
          <button id="themeToggleBtn" class="p-2 text-slate-600 dark:text-slate-300 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 rounded-lg transition" title="화면 테마 변경">
            <i class="fa-solid fa-moon dark:hidden"></i>
            <i class="fa-solid fa-sun hidden dark:inline"></i>
          </button>
        </div>

      </div>
    </header>

    <!-- Main Container -->
    <main class="flex-1 max-w-[1600px] w-full mx-auto p-4 lg:p-8 space-y-6">

      <!-- Alert Banner / Error Box -->
      <div id="errorBox" class="hidden bg-rose-50 dark:bg-rose-950/50 border border-rose-200 dark:border-rose-800 text-rose-800 dark:text-rose-200 px-4 py-3 rounded-xl text-xs sm:text-sm shadow-sm flex items-start gap-3">
        <i class="fa-solid fa-triangle-exclamation text-rose-500 text-lg mt-0.5"></i>
        <div class="flex-1">
          <p id="errorTitle" class="font-bold mb-0.5">데이터를 불러오는 중 오류가 발생했습니다.</p>
          <p id="errorMessage" class="text-rose-600 dark:text-rose-300 whitespace-pre-wrap leading-relaxed"></p>
        </div>
        <button id="closeErrorBtn" class="text-rose-400 hover:text-rose-600"><i class="fa-solid fa-xmark"></i></button>
      </div>

      <!-- Quick Data Switcher Banner -->
      <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-4 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div class="flex items-center gap-3">
          <div class="p-2 bg-indigo-50 dark:bg-indigo-950/60 text-indigo-600 dark:text-indigo-400 rounded-lg shrink-0">
            <i class="fa-solid fa-database text-lg"></i>
          </div>
          <div>
            <div class="text-xs font-semibold text-slate-500 dark:text-slate-400">현재 데이터 소스</div>
            <div id="currentSourceLabel" class="text-sm font-bold text-slate-800 dark:text-slate-100 truncate max-w-xl">
              Google Sheets Live CSV
            </div>
          </div>
        </div>

        <div class="flex flex-wrap items-center gap-2">
          <button id="sampleDatasetBtn1" class="px-3 py-1.5 text-xs font-medium rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 hover:bg-slate-100 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 transition">
            <i class="fa-solid fa-table-cells mr-1 text-slate-400"></i>샘플 시트 A
          </button>
          <button id="sampleDatasetBtn2" class="px-3 py-1.5 text-xs font-medium rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 hover:bg-slate-100 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 transition">
            <i class="fa-solid fa-table-cells mr-1 text-slate-400"></i>샘플 시트 B
          </button>
          <button id="uploadCsvTriggerBtn" class="px-3 py-1.5 text-xs font-medium rounded-lg border border-brand-200 dark:border-brand-900 bg-brand-50 dark:bg-brand-950/50 hover:bg-brand-100 dark:hover:bg-brand-900/80 text-brand-700 dark:text-brand-300 transition">
            <i class="fa-solid fa-file-csv mr-1"></i>내 CSV 업로드
          </button>
        </div>
      </div>

      <!-- KPI Cards Grid -->
      <section class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4">
        
        <!-- KPI 1: Total Records -->
        <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-4 shadow-sm relative overflow-hidden group">
          <div class="flex items-center justify-between mb-2">
            <span class="text-xs font-semibold text-slate-500 dark:text-slate-400">전체 데이터 행</span>
            <span class="p-2 bg-blue-50 dark:bg-blue-950/60 text-blue-600 dark:text-blue-400 rounded-lg">
              <i class="fa-solid fa-list-check text-sm"></i>
            </span>
          </div>
          <div class="text-2xl lg:text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight" id="kRows">-</div>
          <div class="text-[11px] text-slate-400 dark:text-slate-500 mt-1 flex items-center gap-1">
            <i class="fa-solid fa-info-circle"></i> 헤더 제외 데이터 수
          </div>
        </div>

        <!-- KPI 2: Total Columns -->
        <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-4 shadow-sm relative overflow-hidden group">
          <div class="flex items-center justify-between mb-2">
            <span class="text-xs font-semibold text-slate-500 dark:text-slate-400">전체 컬럼 수</span>
            <span class="p-2 bg-indigo-50 dark:bg-indigo-950/60 text-indigo-600 dark:text-indigo-400 rounded-lg">
              <i class="fa-solid fa-columns text-sm"></i>
            </span>
          </div>
          <div class="text-2xl lg:text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight" id="kCols">-</div>
          <div class="text-[11px] text-slate-400 dark:text-slate-500 mt-1 flex items-center gap-1">
            <i class="fa-solid fa-layer-group"></i> 감지된 필드 개수
          </div>
        </div>

        <!-- KPI 3: Data Completeness -->
        <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-4 shadow-sm relative overflow-hidden group">
          <div class="flex items-center justify-between mb-2">
            <span class="text-xs font-semibold text-slate-500 dark:text-slate-400">데이터 완성도</span>
            <span class="p-2 bg-emerald-50 dark:bg-emerald-950/60 text-emerald-600 dark:text-emerald-400 rounded-lg">
              <i class="fa-solid fa-shield-halved text-sm"></i>
            </span>
          </div>
          <div class="text-2xl lg:text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight" id="kQuality">-</div>
          <div class="text-[11px] text-slate-400 dark:text-slate-500 mt-1 flex items-center gap-1">
            <i class="fa-solid fa-check"></i> 채워진 셀 비율
          </div>
        </div>

        <!-- KPI 4: Numeric Fields Detected -->
        <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-4 shadow-sm relative overflow-hidden group">
          <div class="flex items-center justify-between mb-2">
            <span class="text-xs font-semibold text-slate-500 dark:text-slate-400">수치 컬럼</span>
            <span class="p-2 bg-amber-50 dark:bg-amber-950/60 text-amber-600 dark:text-amber-400 rounded-lg">
              <i class="fa-solid fa-arrow-trend-up text-sm"></i>
            </span>
          </div>
          <div class="text-2xl lg:text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight" id="kNumeric">-</div>
          <div class="text-[11px] text-slate-400 dark:text-slate-500 mt-1 truncate" id="numericHint">자동 감지</div>
        </div>

        <!-- KPI 5: Refresh Interval / Sync Speed -->
        <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-4 shadow-sm relative overflow-hidden group col-span-2 md:col-span-1">
          <div class="flex items-center justify-between mb-2">
            <span class="text-xs font-semibold text-slate-500 dark:text-slate-400">동기화 주기</span>
            <span class="p-2 bg-purple-50 dark:bg-purple-950/60 text-purple-600 dark:text-purple-400 rounded-lg">
              <i class="fa-solid fa-bolt text-sm"></i>
            </span>
          </div>
          <div class="text-2xl lg:text-3xl font-extrabold text-slate-900 dark:text-white tracking-tight">30s</div>
          <div class="text-[11px] text-slate-400 dark:text-slate-500 mt-1 flex items-center gap-1">
            <i class="fa-solid fa-arrows-rotate"></i> 실시간 자동 폴링 중
          </div>
        </div>

      </section>

      <!-- Visual Analytics Grid (4 Charts) -->
      <section class="grid grid-cols-1 lg:grid-cols-2 gap-6">

        <!-- Chart Card 1: Categorical Distribution -->
        <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-5 shadow-sm flex flex-col justify-between">
          <div class="flex items-start justify-between gap-4 mb-4">
            <div>
              <div class="flex items-center gap-2">
                <i class="fa-solid fa-chart-pie text-brand-500 text-sm"></i>
                <h3 id="chart1Title" class="text-base font-bold text-slate-900 dark:text-white">주요 항목 분포</h3>
              </div>
              <p id="chart1Desc" class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">범주형 컬럼 분포 분석</p>
            </div>
            <div class="flex items-center gap-1">
              <button id="toggleChart1Type" class="text-xs text-slate-500 hover:text-slate-800 dark:hover:text-slate-200 bg-slate-100 dark:bg-slate-800 px-2 py-1 rounded-md transition" title="차트 유형 변경">
                <i class="fa-solid fa-chart-column"></i>
              </button>
            </div>
          </div>
          <div class="relative w-full h-[280px]">
            <canvas id="chart1"></canvas>
          </div>
        </div>

        <!-- Chart Card 2: Numeric Metrics Summary -->
        <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-5 shadow-sm flex flex-col justify-between">
          <div class="flex items-start justify-between gap-4 mb-4">
            <div>
              <div class="flex items-center gap-2">
                <i class="fa-solid fa-chart-simple text-emerald-500 text-sm"></i>
                <h3 id="chart2Title" class="text-base font-bold text-slate-900 dark:text-white">수치 현황 (평균)</h3>
              </div>
              <p id="chart2Desc" class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">수치형 데이터 평균 및 범위</p>
            </div>
          </div>
          <div class="relative w-full h-[280px]">
            <canvas id="chart2"></canvas>
          </div>
        </div>

        <!-- Chart Card 3: Secondary Breakdown -->
        <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-5 shadow-sm flex flex-col justify-between">
          <div class="flex items-start justify-between gap-4 mb-4">
            <div>
              <div class="flex items-center gap-2">
                <i class="fa-solid fa-chart-bar text-purple-500 text-sm"></i>
                <h3 id="chart3Title" class="text-base font-bold text-slate-900 dark:text-white">추가 세부 분포</h3>
              </div>
              <p id="chart3Desc" class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">서브 범주 분석</p>
            </div>
          </div>
          <div class="relative w-full h-[280px]">
            <canvas id="chart3"></canvas>
          </div>
        </div>

        <!-- Chart Card 4: Time Series & Trend Analytics -->
        <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl p-5 shadow-sm flex flex-col justify-between">
          <div class="flex items-start justify-between gap-4 mb-4">
            <div>
              <div class="flex items-center gap-2">
                <i class="fa-solid fa-chart-line text-amber-500 text-sm"></i>
                <h3 id="chart4Title" class="text-base font-bold text-slate-900 dark:text-white">시계열 추이 분석</h3>
              </div>
              <p id="chart4Desc" class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">날짜 및 수치 컬럼 연동 시계열</p>
            </div>
          </div>
          <div class="relative w-full h-[280px]">
            <canvas id="chart4"></canvas>
          </div>
        </div>

      </section>

      <!-- Interactive Raw Data Table Section -->
      <section class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl shadow-sm overflow-hidden">
        
        <!-- Table Control Toolbar -->
        <div class="p-4 sm:p-5 border-b border-slate-200 dark:border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-3">
          <div class="flex flex-1 flex-wrap items-center gap-2 sm:gap-3">
            <!-- Search Box -->
            <div class="relative flex-1 min-w-[220px]">
              <i class="fa-solid fa-magnifying-glass absolute left-3.5 top-1/2 -translate-y-1/2 text-slate-400 text-xs"></i>
              <input id="searchInput" type="search" placeholder="전체 컬럼 실시간 검색..." class="w-full pl-9 pr-4 py-2 bg-slate-50 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700/80 rounded-xl text-xs sm:text-sm focus:outline-none focus:ring-2 focus:ring-brand-500 transition text-slate-800 dark:text-slate-100 placeholder-slate-400" />
            </div>

            <!-- Specific Column Filter Dropdown -->
            <select id="columnFilter" class="py-2 px-3 bg-slate-50 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700/80 rounded-xl text-xs sm:text-sm text-slate-800 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-brand-500 transition">
              <option value="">모든 컬럼 대상 검색</option>
            </select>

            <!-- Page Size Dropdown -->
            <select id="pageSizeSelect" class="py-2 px-3 bg-slate-50 dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700/80 rounded-xl text-xs sm:text-sm text-slate-800 dark:text-slate-100 focus:outline-none focus:ring-2 focus:ring-brand-500 transition">
              <option value="15">15개씩 보기</option>
              <option value="30" selected>30개씩 보기</option>
              <option value="50">50개씩 보기</option>
              <option value="100">100개씩 보기</option>
            </select>
          </div>

          <div class="flex items-center gap-2 shrink-0">
            <!-- CSV Download Button -->
            <button id="downloadBtn" class="px-3.5 py-2 bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 rounded-xl text-xs font-bold transition flex items-center gap-2">
              <i class="fa-solid fa-download text-brand-500"></i>
              <span>CSV 다운로드</span>
            </button>
          </div>
        </div>

        <!-- Table View -->
        <div class="overflow-x-auto max-h-[600px] relative">
          <table class="w-full text-left border-collapse text-xs sm:text-sm">
            <thead>
              <tr id="thead" class="sticky top-0 bg-slate-100/95 dark:bg-slate-800/95 backdrop-blur-md text-slate-600 dark:text-slate-300 font-semibold border-b border-slate-200 dark:border-slate-700 select-none z-10">
                <!-- Dynamic Header Cells generated via JavaScript -->
              </tr>
            </thead>
            <tbody id="tbody" class="divide-y divide-slate-100 dark:divide-slate-800/60 text-slate-700 dark:text-slate-300">
              <!-- Dynamic Rows -->
            </tbody>
          </table>

          <!-- Empty State Indicator -->
          <div id="empty" class="hidden py-16 text-center text-slate-400 dark:text-slate-500">
            <i class="fa-solid fa-folder-open text-4xl mb-3 opacity-40"></i>
            <p class="text-sm font-medium">검색 조건에 일치하는 데이터가 없습니다.</p>
          </div>
        </div>

        <!-- Pagination Controls -->
        <div class="p-4 border-t border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-900/50 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs text-slate-500 dark:text-slate-400">
          <div id="paginationSummary">데이터 로드 중...</div>
          <div class="flex items-center gap-1" id="paginationButtons">
            <!-- Pagination buttons -->
          </div>
        </div>

      </section>

    </main>

    <!-- Footer Status -->
    <footer class="border-t border-slate-200 dark:border-slate-800 py-4 px-6 text-center text-xs text-slate-400 dark:text-slate-600">
      <div class="max-w-[1600px] mx-auto flex flex-col sm:flex-row justify-between items-center gap-2">
        <div>Google Sheets Live CSV 연동 대시보드 Engine</div>
        <div id="footerMetaText">-</div>
      </div>
    </footer>

  </div>

  <!-- Modal 1: Data Source Settings Modal -->
  <div id="settingsModal" class="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-sm hidden items-center justify-center p-4">
    <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl w-full max-w-xl p-6 shadow-2xl space-y-5 animate-in fade-in zoom-in-95 duration-200">
      
      <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-4">
        <h3 class="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
          <i class="fa-solid fa-link text-brand-500"></i> 데이터 소스 설정
        </h3>
        <button id="closeSettingsBtn" class="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 text-lg">
          <i class="fa-solid fa-xmark"></i>
        </button>
      </div>

      <div class="space-y-4 text-xs sm:text-sm">
        <div>
          <label class="block font-semibold text-slate-700 dark:text-slate-300 mb-1">
            Google Sheets 게시된 CSV URL
          </label>
          <input id="customCsvUrlInput" type="url" placeholder="https://docs.google.com/spreadsheets/d/e/.../pub?output=csv" class="w-full px-3.5 py-2.5 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl focus:ring-2 focus:ring-brand-500 outline-none transition text-slate-900 dark:text-slate-100" />
          <p class="text-[11px] text-slate-400 dark:text-slate-500 mt-1">
            * 구글 시트 메뉴 [파일] -&gt; [공유] -&gt; [웹에 게시]에서 형식으로 '웹페이지(CSV)'를 선택 후 URL을 입력하세요.
          </p>
        </div>

        <div>
          <label class="block font-semibold text-slate-700 dark:text-slate-300 mb-1">
            자동 갱신 주기 (초)
          </label>
          <select id="refreshIntervalSelect" class="w-full px-3.5 py-2.5 bg-slate-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-xl focus:ring-2 focus:ring-brand-500 outline-none transition text-slate-900 dark:text-slate-100">
            <option value="10">10초마다 갱신</option>
            <option value="30" selected>30초마다 갱신 (기본값)</option>
            <option value="60">1분마다 갱신</option>
            <option value="300">5분마다 갱신</option>
          </select>
        </div>
      </div>

      <div class="flex justify-end gap-2 pt-2 border-t border-slate-100 dark:border-slate-800">
        <button id="cancelSettingsBtn" class="px-4 py-2 text-xs font-semibold rounded-xl text-slate-600 dark:text-slate-300 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 transition">취소</button>
        <button id="saveSettingsBtn" class="px-4 py-2 text-xs font-semibold rounded-xl text-white bg-brand-600 hover:bg-brand-700 transition shadow-md shadow-brand-500/20">저장 및 적용</button>
      </div>

    </div>
  </div>

  <!-- Modal 2: CSV Upload Modal -->
  <div id="uploadModal" class="fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-sm hidden items-center justify-center p-4">
    <div class="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-2xl w-full max-w-lg p-6 shadow-2xl space-y-5">
      
      <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-4">
        <h3 class="text-base font-bold text-slate-900 dark:text-white flex items-center gap-2">
          <i class="fa-solid fa-file-csv text-brand-500"></i> 내 로컬 CSV 파일 가져오기
        </h3>
        <button id="closeUploadBtn" class="text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 text-lg">
          <i class="fa-solid fa-xmark"></i>
        </button>
      </div>

      <!-- Dropzone -->
      <div id="dropzone" class="border-2 border-dashed border-slate-300 dark:border-slate-700 hover:border-brand-500 dark:hover:border-brand-500 rounded-2xl p-8 text-center transition cursor-pointer bg-slate-50/50 dark:bg-slate-800/30 flex flex-col items-center justify-center gap-3">
        <div class="p-4 bg-brand-50 dark:bg-brand-950/60 text-brand-600 dark:text-brand-400 rounded-full">
          <i class="fa-solid fa-cloud-arrow-up text-2xl"></i>
        </div>
        <div>
          <p class="text-sm font-bold text-slate-800 dark:text-slate-200">클릭하거나 CSV 파일을 이곳에 드래그하세요</p>
          <p class="text-xs text-slate-400 mt-1">UTF-8 인코딩 지원</p>
        </div>
        <input id="csvFileInput" type="file" accept=".csv" class="hidden" />
      </div>

      <div class="flex justify-end pt-2">
        <button id="cancelUploadBtn" class="px-4 py-2 text-xs font-semibold rounded-xl text-slate-600 dark:text-slate-300 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 transition">닫기</button>
      </div>

    </div>
  </div>

  <script>
  // Default Sample Datasets
  const SAMPLE_SHEETS = {
    A: 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQGeoZPZ0xvIqZ9vkTFQ4R-zTLeRvYhByddcAxYz7NDgTQ4qAImOqdNxXHHSnMfQMqxE6KJYOqwJx4Y/pub?output=csv',
    B: 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQ9nCMJi93wXJALqitxp3L-LFPt4T5GMUxBmcFGSErcl5t7-UewuZ1dv7f3VyosUjwIrwNLt_s6_7DN/pub?output=csv'
  };

  // Application Global State
  let currentCsvUrl = SAMPLE_SHEETS.A;
  let refreshSeconds = 30;
  let countdown = refreshSeconds;
  let isPaused = false;
  let timerId = null;

  let rawRows = [];
  let headers = [];
  let filteredRows = [];
  let detectedTypes = { numeric: [], date: [], categorical: [] };

  let charts = {};
  let sortState = { key: null, asc: true };
  let currentPage = 1;
  let pageSize = 30;
  let chart1Type = 'bar'; // default chart 1 style

  // Robust CSV Parser (Supports escaped quotes and newlines)
  function parseCSV(text) {
    const out = [];
    let row = [], cell = '', inQuotes = false;
    for (let i = 0; i < text.length; i++) {
      const c = text[i], n = text[i + 1];
      if (c === '"') {
        if (inQuotes && n === '"') { cell += '"'; i++; }
        else inQuotes = !inQuotes;
      } else if (c === ',' && !inQuotes) {
        row.push(cell); cell = '';
      } else if ((c === '\n' || c === '\r') && !inQuotes) {
        if (c === '\r' && n === '\n') i++;
        row.push(cell); out.push(row); row = []; cell = '';
      } else {
        cell += c;
      }
    }
    if (cell.length || row.length) { row.push(cell); out.push(row); }
    return out.filter(r => r.some(v => String(v).trim() !== ''));
  }

  // Normalize Matrix Data to Array of Objects
  function normalizeData(matrix) {
    if (!matrix.length) return { headers: [], rows: [] };
    let hs = matrix[0].map((h, i) => String(h).trim() || `컬럼${i + 1}`);
    const seen = {};
    hs = hs.map(h => {
      seen[h] = (seen[h] || 0) + 1;
      return seen[h] > 1 ? `${h}_${seen[h]}` : h;
    });
    const rs = matrix.slice(1).map(r => {
      const o = {};
      hs.forEach((h, i) => o[h] = (r[i] ?? '').trim());
      return o;
    }).filter(o => Object.values(o).some(v => v !== ''));
    return { headers: hs, rows: rs };
  }

  // Value Type Helpers
  function toNumber(v) {
    if (v === null || v === undefined || String(v).trim() === '') return null;
    const s = String(v).replace(/[,₩$% ]/g, '').trim();
    if (!/^[-+]?\d*\.?\d+$/.test(s)) return null;
    const n = Number(s);
    return Number.isFinite(n) ? n : null;
  }

  function toDate(v) {
    const s = String(v || '').trim();
    if (!s || /^\d{1,3}$/.test(s)) return null;
    const normalized = s.replace(/\./g, '-').replace(/\//g, '-').replace(/년|월/g, '-').replace(/일/g, '').replace(/\s+/g, '');
    const d = new Date(normalized);
    return isNaN(d.getTime()) ? null : d;
  }

  // Column Auto-Type Detector
  function detectTypes() {
    const types = { numeric: [], date: [], categorical: [] };
    headers.forEach(h => {
      const vals = rawRows.map(r => r[h]).filter(v => String(v).trim() !== '');
      if (!vals.length) return;
      const sample = vals.slice(0, Math.min(300, vals.length));
      const numRatio = sample.filter(v => toNumber(v) !== null).length / sample.length;
      const dateRatio = sample.filter(v => toDate(v) !== null).length / sample.length;
      const unique = new Set(sample).size;

      if (numRatio >= 0.85) {
        types.numeric.push(h);
      } else if (dateRatio >= 0.80) {
        types.date.push(h);
      } else if (unique <= Math.min(30, Math.max(6, sample.length * 0.4))) {
        types.categorical.push(h);
      }
    });
    return types;
  }

  // Helper: Count Occurrences for Categorical Charts
  function countBy(col, limit = 10) {
    const m = new Map();
    rawRows.forEach(r => {
      const v = (r[col] || '').trim() || '(빈 값)';
      m.set(v, (m.get(v) || 0) + 1);
    });
    return [...m.entries()].sort((a, b) => b[1] - a[1]).slice(0, limit);
  }

  // Chart Helper: Destroy existing chart
  function destroyChart(id) {
    if (charts[id]) {
      charts[id].destroy();
      delete charts[id];
    }
  }

  function getThemeColors() {
    const isDark = document.documentElement.classList.contains('dark');
    return {
      textColor: isDark ? '#94a3b8' : '#475569',
      gridColor: isDark ? 'rgba(51, 65, 85, 0.4)' : 'rgba(226, 232, 240, 0.8)',
      brand: '#3b82f6',
      emerald: '#10b981',
      purple: '#8b5cf6',
      amber: '#f59e0b',
      palette: ['#3b82f6', '#10b981', '#8b5cf6', '#f59e0b', '#ec4899', '#06b6d4', '#6366f1', '#f97316']
    };
  }

  // Chart 1: Major Categorical Bar/Donut Chart
  function renderChart1(col) {
    destroyChart('chart1');
    const titleEl = document.getElementById('chart1Title');
    const descEl = document.getElementById('chart1Desc');
    const colors = getThemeColors();

    if (!col) {
      titleEl.textContent = '범주 데이터 없음';
      descEl.textContent = '분석할 범주형 컬럼이 감지되지 않았습니다.';
      return;
    }

    const data = countBy(col);
    titleEl.textContent = `${col} 분포`;
    descEl.textContent = `상위 ${data.length}개 항목 건수`;

    const ctx = document.getElementById('chart1').getContext('2d');
    charts['chart1'] = new Chart(ctx, {
      type: chart1Type,
      data: {
        labels: data.map(x => x[0]),
        datasets: [{
          label: '건수',
          data: data.map(x => x[1]),
          backgroundColor: chart1Type === 'doughnut' ? colors.palette : colors.brand,
          borderRadius: chart1Type === 'bar' ? 6 : 0,
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: chart1Type === 'doughnut', labels: { color: colors.textColor, font: { family: 'Inter' } } }
        },
        scales: chart1Type === 'bar' ? {
          y: { beginAtZero: true, ticks: { color: colors.textColor, precision: 0 }, grid: { color: colors.gridColor } },
          x: { ticks: { color: colors.textColor, maxRotation: 30 }, grid: { display: false } }
        } : {}
      }
    });
  }

  // Chart 2: Numeric Columns Mean Summary Chart
  function renderChart2(types) {
    destroyChart('chart2');
    const titleEl = document.getElementById('chart2Title');
    const descEl = document.getElementById('chart2Desc');
    const colors = getThemeColors();

    const cols = types.numeric.slice(0, 8);
    if (!cols.length) {
      titleEl.textContent = '수치 데이터 없음';
      descEl.textContent = '수치형 컬럼이 감지되지 않았습니다.';
      return;
    }

    const data = cols.map(c => {
      const valid = rawRows.map(r => toNumber(r[c])).filter(v => v !== null);
      const avg = valid.length ? valid.reduce((s, v) => s + v, 0) / valid.length : 0;
      return [c, avg];
    });

    titleEl.textContent = '수치 컬럼 평균 지표';
    descEl.textContent = `감지된 ${cols.length}개 수치 항목 평균`;

    const ctx = document.getElementById('chart2').getContext('2d');
    charts['chart2'] = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: data.map(x => x[0]),
        datasets: [{
          label: '평균값',
          data: data.map(x => x[1]),
          backgroundColor: colors.emerald,
          borderRadius: 6,
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          y: { beginAtZero: true, ticks: { color: colors.textColor }, grid: { color: colors.gridColor } },
          x: { ticks: { color: colors.textColor, maxRotation: 30 }, grid: { display: false } }
        }
      }
    });
  }

  // Chart 3: Secondary Categorical Breakdown
  function renderChart3(col) {
    destroyChart('chart3');
    const titleEl = document.getElementById('chart3Title');
    const descEl = document.getElementById('chart3Desc');
    const colors = getThemeColors();

    if (!col) {
      titleEl.textContent = '추가 세부 범주 없음';
      descEl.textContent = '두 번째 범주형 컬럼이 감지되지 않았습니다.';
      return;
    }

    const data = countBy(col, 8);
    titleEl.textContent = `${col} 세부 분석`;
    descEl.textContent = `항목별 건수 비율`;

    const ctx = document.getElementById('chart3').getContext('2d');
    charts['chart3'] = new Chart(ctx, {
      type: 'bar',
      data: {
        labels: data.map(x => x[0]),
        datasets: [{
          label: '건수',
          data: data.map(x => x[1]),
          backgroundColor: colors.purple,
          borderRadius: 6
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          x: { beginAtZero: true, ticks: { color: colors.textColor, precision: 0 }, grid: { color: colors.gridColor } },
          y: { ticks: { color: colors.textColor }, grid: { display: false } }
        }
      }
    });
  }

  // Chart 4: Time Series & Trend Chart
  function renderChart4(types) {
    destroyChart('chart4');
    const titleEl = document.getElementById('chart4Title');
    const descEl = document.getElementById('chart4Desc');
    const colors = getThemeColors();

    if (!types.date.length || !types.numeric.length) {
      titleEl.textContent = '시계열 조건 미충족';
      descEl.textContent = '날짜형 컬럼과 수치형 컬럼이 모두 존재할 때 시계열 추이가 생성됩니다.';
      return;
    }

    const dc = types.date[0];
    const nc = types.numeric[0];
    const map = new Map();

    rawRows.forEach(r => {
      const d = toDate(r[dc]);
      const n = toNumber(r[nc]);
      if (!d || n === null) return;
      const key = d.toISOString().slice(0, 10);
      if (!map.has(key)) map.set(key, { sum: 0, count: 0 });
      const x = map.get(key);
      x.sum += n; x.count++;
    });

    const data = [...map.entries()]
      .sort((a, b) => a[0].localeCompare(b[0]))
      .map(([k, v]) => [k, v.sum / v.count]);

    titleEl.textContent = `${nc} 일별 추이`;
    descEl.textContent = `${dc} 기준 일자별 평균값`;

    const ctx = document.getElementById('chart4').getContext('2d');
    charts['chart4'] = new Chart(ctx, {
      type: 'line',
      data: {
        labels: data.map(x => x[0]),
        datasets: [{
          label: nc,
          data: data.map(x => x[1]),
          borderColor: colors.amber,
          backgroundColor: 'rgba(245, 158, 11, 0.15)',
          fill: true,
          tension: 0.3,
          pointRadius: 3,
          pointHoverRadius: 6
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          x: { ticks: { color: colors.textColor, maxTicksLimit: 10 }, grid: { color: colors.gridColor } },
          y: { ticks: { color: colors.textColor }, grid: { color: colors.gridColor } }
        }
      }
    });
  }

  // Update KPIs Bar
  function updateKPIs(types) {
    document.getElementById('kRows').textContent = rawRows.length.toLocaleString();
    document.getElementById('kCols').textContent = headers.length.toLocaleString();
    
    const totalCells = rawRows.length * headers.length;
    let filledCells = 0;
    rawRows.forEach(r => headers.forEach(h => {
      if (String(r[h] ?? '').trim() !== '') filledCells++;
    }));
    
    document.getElementById('kQuality').textContent = totalCells ? `${(filledCells / totalCells * 100).toFixed(1)}%` : '-';
    document.getElementById('kNumeric').textContent = types.numeric.length.toLocaleString();
    document.getElementById('numericHint').textContent = types.numeric.length ? types.numeric.slice(0, 2).join(', ') : '수치 항목 없음';
    
    const nowStr = new Date().toLocaleTimeString('ko-KR', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
    document.getElementById('dataTimeText').textContent = `최근 수신: ${nowStr}`;
    document.getElementById('footerMetaText').textContent = `${rawRows.length.toLocaleString()} 행 · ${headers.length.toLocaleString()} 열 · 실시간 감지 완료`;
  }

  // Table Rendering with Sorting & Pagination
  function renderTable() {
    const q = document.getElementById('searchInput').value.trim().toLowerCase();
    const cf = document.getElementById('columnFilter').value;

    filteredRows = rawRows.filter(r => {
      if (!q) return true;
      if (cf) return String(r[cf] ?? '').toLowerCase().includes(q);
      return headers.some(h => String(r[h] ?? '').toLowerCase().includes(q));
    });

    if (sortState.key) {
      const k = sortState.key;
      const asc = sortState.asc;
      filteredRows.sort((a, b) => {
        const na = toNumber(a[k]), nb = toNumber(b[k]);
        let cmp;
        if (na !== null && nb !== null) cmp = na - nb;
        else cmp = String(a[k] ?? '').localeCompare(String(b[k] ?? ''), 'ko');
        return asc ? cmp : -cmp;
      });
    }

    // Render Table Header
    const thead = document.getElementById('thead');
    thead.innerHTML = '<tr>' + headers.map(h => {
      const isSorted = sortState.key === h;
      const arrow = isSorted ? (sortState.asc ? ' ▲' : ' ▼') : '';
      return `<th data-key="${escapeHTML(h)}" class="px-4 py-3 cursor-pointer hover:bg-slate-200/60 dark:hover:bg-slate-700/60 transition whitespace-nowrap">
        ${escapeHTML(h)}<span class="text-brand-500 font-bold">${arrow}</span>
      </th>`;
    }).join('') + '</tr>';

    // Pagination Calculation
    const total = filteredRows.length;
    const totalPages = Math.ceil(total / pageSize) || 1;
    if (currentPage > totalPages) currentPage = totalPages;

    const startIdx = (currentPage - 1) * pageSize;
    const endIdx = Math.min(startIdx + pageSize, total);
    const pageRows = filteredRows.slice(startIdx, endIdx);

    // Render Body Rows
    const tbody = document.getElementById('tbody');
    tbody.innerHTML = pageRows.map(r => '<tr>' + headers.map(h => {
      return `<td class="px-4 py-2.5 whitespace-nowrap border-b border-slate-100 dark:border-slate-800/60">${escapeHTML(r[h] ?? '')}</td>`;
    }).join('') + '</tr>').join('');

    document.getElementById('empty').style.display = total === 0 ? 'block' : 'none';

    // Pagination Summary Text & Buttons
    document.getElementById('paginationSummary').textContent = total > 0 
      ? `전체 ${total.toLocaleString()}개 중 ${startIdx + 1}-${endIdx} 표시 (페이지 ${currentPage}/${totalPages})`
      : '표시할 데이터 없음';

    renderPaginationButtons(totalPages);

    // Bind Column Header Click Events for Sorting
    document.querySelectorAll('th[data-key]').forEach(th => {
      th.addEventListener('click', () => {
        const k = th.dataset.key;
        if (sortState.key === k) {
          sortState.asc = !sortState.asc;
        } else {
          sortState.key = k;
          sortState.asc = true;
        }
        renderTable();
      });
    });
  }

  function renderPaginationButtons(totalPages) {
    const container = document.getElementById('paginationButtons');
    container.innerHTML = '';

    if (totalPages <= 1) return;

    const prevBtn = document.createElement('button');
    prevBtn.className = `px-2.5 py-1 rounded-lg border border-slate-200 dark:border-slate-700 ${currentPage === 1 ? 'opacity-40 cursor-not-allowed' : 'hover:bg-slate-100 dark:hover:bg-slate-800'}`;
    prevBtn.innerHTML = '<i class="fa-solid fa-chevron-left"></i>';
    prevBtn.disabled = currentPage === 1;
    prevBtn.onclick = () => { currentPage--; renderTable(); };
    container.appendChild(prevBtn);

    // Dynamic Page Number Buttons
    let pages = [];
    for (let p = 1; p <= totalPages; p++) {
      if (p === 1 || p === totalPages || (p >= currentPage - 2 && p <= currentPage + 2)) {
        pages.push(p);
      }
    }

    pages.forEach(p => {
      const btn = document.createElement('button');
      btn.className = `px-3 py-1 rounded-lg border font-semibold ${p === currentPage ? 'bg-brand-600 text-white border-brand-600' : 'border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-800'}`;
      btn.textContent = p;
      btn.onclick = () => { currentPage = p; renderTable(); };
      container.appendChild(btn);
    });

    const nextBtn = document.createElement('button');
    nextBtn.className = `px-2.5 py-1 rounded-lg border border-slate-200 dark:border-slate-700 ${currentPage === totalPages ? 'opacity-40 cursor-not-allowed' : 'hover:bg-slate-100 dark:hover:bg-slate-800'}`;
    nextBtn.innerHTML = '<i class="fa-solid fa-chevron-right"></i>';
    nextBtn.disabled = currentPage === totalPages;
    nextBtn.onclick = () => { currentPage++; renderTable(); };
    container.appendChild(nextBtn);
  }

  function escapeHTML(s) {
    return String(s).replace(/[&<>"']/g, m => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[m]));
  }

  function populateColumnFilter() {
    const el = document.getElementById('columnFilter');
    const oldVal = el.value;
    el.innerHTML = '<option value="">모든 컬럼 대상 검색</option>' + headers.map(h => `<option value="${escapeHTML(h)}">${escapeHTML(h)} 검색</option>`).join('');
    if (headers.includes(oldVal)) el.value = oldVal;
  }

  function renderAll() {
    detectedTypes = detectTypes();
    updateKPIs(detectedTypes);

    const cat1 = detectedTypes.categorical[0] || headers.find(h => !detectedTypes.numeric.includes(h) && !detectedTypes.date.includes(h));
    const cat2 = detectedTypes.categorical[1] || detectedTypes.categorical[0];

    renderChart1(cat1);
    renderChart2(detectedTypes);
    renderChart3(cat2);
    renderChart4(detectedTypes);

    populateColumnFilter();
    renderTable();
  }

  // Load Data via Fetch with Error Boundary & Cache Busting
  async function loadData() {
    const errorBox = document.getElementById('errorBox');
    const spinner = document.getElementById('refreshSpinner');
    const statusText = document.getElementById('statusText');
    
    spinner.classList.add('fa-spin');
    statusText.textContent = '갱신 중';

    try {
      const sep = currentCsvUrl.includes('?') ? '&' : '?';
      const fetchUrl = currentCsvUrl + sep + '_ts=' + Date.now();
      
      const res = await fetch(fetchUrl, { cache: 'no-store' });
      if (!res.ok) throw new Error(`HTTP ${res.status}: 데이터를 불러올 수 없습니다.`);
      
      const text = await res.text();
      const matrix = parseCSV(text);
      const data = normalizeData(matrix);

      if (!data.headers.length) throw new Error('유효한 CSV 헤더를 찾지 못했습니다.');

      headers = data.headers;
      rawRows = data.rows;

      renderAll();

      errorBox.classList.add('hidden');
      statusText.textContent = '정상 연동';
      countdown = refreshSeconds;
    } catch (err) {
      statusText.textContent = '연동 오류';
      errorBox.classList.remove('hidden');
      document.getElementById('errorMessage').textContent = err.message + '\n\n* 참고: 로컬 file:// 모드에서 CORS 제한이 발생할 수 있으므로 웹서버(GitHub Pages, Vercel 등) 환경이나 모달에서 직접 CSV 파일을 업로드하여 테스트할 수 있습니다.';
    } finally {
      spinner.classList.remove('fa-spin');
    }
  }

  // Download CSV
  function downloadCSV() {
    if (!headers.length) return;
    const src = filteredRows.length ? filteredRows : rawRows;
    const esc = v => `"${String(v ?? '').replace(/"/g, '""')}"`;
    const csvContent = '\ufeff' + [headers.map(esc).join(','), ...src.map(r => headers.map(h => esc(r[h])).join(','))].join('\r\n');
    
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const a = document.createElement('a');
    a.href = URL.createObjectURL(blob);
    a.download = `dashboard_data_${new Date().toISOString().slice(0, 10)}.csv`;
    a.click();
    URL.revokeObjectURL(a.href);
  }

  // Theme Toggle Handler
  function initTheme() {
    const isDark = localStorage.getItem('theme') === 'dark' || (!('theme' in localStorage) && window.matchMedia('(prefers-color-scheme: dark)').matches);
    if (isDark) document.documentElement.classList.add('dark');
    else document.documentElement.classList.remove('dark');
  }

  document.getElementById('themeToggleBtn').addEventListener('click', () => {
    document.documentElement.classList.toggle('dark');
    const isDark = document.documentElement.classList.contains('dark');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
    if (rawRows.length) renderAll(); // Refresh charts for theme color match
  });

  // Modal Dialog Handlers
  const settingsModal = document.getElementById('settingsModal');
  const uploadModal = document.getElementById('uploadModal');

  document.getElementById('openSettingsBtn').addEventListener('click', () => {
    document.getElementById('customCsvUrlInput').value = currentCsvUrl;
    document.getElementById('refreshIntervalSelect').value = refreshSeconds;
    settingsModal.classList.remove('hidden');
    settingsModal.classList.add('flex');
  });

  const closeSettings = () => { settingsModal.classList.add('hidden'); settingsModal.classList.remove('flex'); };
  document.getElementById('closeSettingsBtn').addEventListener('click', closeSettings);
  document.getElementById('cancelSettingsBtn').addEventListener('click', closeSettings);

  document.getElementById('saveSettingsBtn').addEventListener('click', () => {
    const inputUrl = document.getElementById('customCsvUrlInput').value.trim();
    if (inputUrl) {
      currentCsvUrl = inputUrl;
      document.getElementById('currentSourceLabel').textContent = inputUrl;
    }
    refreshSeconds = parseInt(document.getElementById('refreshIntervalSelect').value, 10) || 30;
    countdown = refreshSeconds;
    closeSettings();
    loadData();
  });

  // Local File Drag & Drop Upload
  document.getElementById('uploadCsvTriggerBtn').addEventListener('click', () => {
    uploadModal.classList.remove('hidden');
    uploadModal.classList.add('flex');
  });

  const closeUpload = () => { uploadModal.classList.add('hidden'); uploadModal.classList.remove('flex'); };
  document.getElementById('closeUploadBtn').addEventListener('click', closeUpload);
  document.getElementById('cancelUploadBtn').addEventListener('click', closeUpload);

  const dropzone = document.getElementById('dropzone');
  const fileInput = document.getElementById('csvFileInput');

  dropzone.addEventListener('click', () => fileInput.click());
  dropzone.addEventListener('dragover', (e) => { e.preventDefault(); dropzone.classList.add('border-brand-500'); });
  dropzone.addEventListener('dragleave', () => dropzone.classList.remove('border-brand-500'));
  dropzone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropzone.classList.remove('border-brand-500');
    if (e.dataTransfer.files.length) handleFile(e.dataTransfer.files[0]);
  });
  fileInput.addEventListener('change', (e) => {
    if (e.target.files.length) handleFile(e.target.files[0]);
  });

  function handleFile(file) {
    if (!file.name.endsWith('.csv')) {
      alert('CSV 파일만 지원됩니다.');
      return;
    }
    const reader = new FileReader();
    reader.onload = (e) => {
      const text = e.target.result;
      const matrix = parseCSV(text);
      const data = normalizeData(matrix);
      if (!data.headers.length) {
        alert('유효한 데이터가 없습니다.');
        return;
      }
      headers = data.headers;
      rawRows = data.rows;
      document.getElementById('currentSourceLabel').textContent = `로컬 파일: ${file.name}`;
      closeUpload();
      renderAll();
    };
    reader.readAsText(file, 'UTF-8');
  }

  // Quick Preset Sample Datasets
  document.getElementById('sampleDatasetBtn1').addEventListener('click', () => {
    currentCsvUrl = SAMPLE_SHEETS.A;
    document.getElementById('currentSourceLabel').textContent = '샘플 시트 A (Google Sheets)';
    loadData();
  });

  document.getElementById('sampleDatasetBtn2').addEventListener('click', () => {
    currentCsvUrl = SAMPLE_SHEETS.B;
    document.getElementById('currentSourceLabel').textContent = '샘플 시트 B (Google Sheets)';
    loadData();
  });

  // Chart 1 Type Toggle (Bar <-> Doughnut)
  document.getElementById('toggleChart1Type').addEventListener('click', () => {
    chart1Type = chart1Type === 'bar' ? 'doughnut' : 'bar';
    const cat = detectedTypes.categorical[0] || headers.find(h => !detectedTypes.numeric.includes(h));
    renderChart1(cat);
  });

  // Refresh & Search Controls Listener
  document.getElementById('refreshBtn').addEventListener('click', () => {
    countdown = refreshSeconds;
    loadData();
  });

  document.getElementById('pauseBtn').addEventListener('click', () => {
    isPaused = !isPaused;
    const icon = document.getElementById('pauseIcon');
    icon.className = isPaused ? 'fa-solid fa-play' : 'fa-solid fa-pause';
  });

  document.getElementById('searchInput').addEventListener('input', () => { currentPage = 1; renderTable(); });
  document.getElementById('columnFilter').addEventListener('change', () => { currentPage = 1; renderTable(); });
  document.getElementById('pageSizeSelect').addEventListener('change', (e) => {
    pageSize = parseInt(e.target.value, 10);
    currentPage = 1;
    renderTable();
  });
  document.getElementById('downloadBtn').addEventListener('click', downloadCSV);
  document.getElementById('closeErrorBtn').addEventListener('click', () => {
    document.getElementById('errorBox').classList.add('hidden');
  });

  // 1-second Countdown Interval
  setInterval(() => {
    if (isPaused) return;
    countdown--;
    if (countdown <= 0) {
      loadData();
      countdown = refreshSeconds;
    }
    document.getElementById('countdown').textContent = countdown;
  }, 1000);

  // Initialize Theme and Initial Load
  initTheme();
  loadData();
  </script>
</body>
</html>
