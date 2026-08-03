DASHBOARD_HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VibeSaver.ai - 실시간 반값 API 마진 & 토큰 절감 대시보드</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-primary: #0a0e17;
            --bg-card: rgba(18, 26, 41, 0.75);
            --border-color: rgba(255, 255, 255, 0.08);
            --accent-cyan: #00f2fe;
            --accent-blue: #4facfe;
            --accent-green: #00e676;
            --accent-purple: #9d4edd;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
        }
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Inter', -apple-system, sans-serif;
        }
        body {
            background: radial-gradient(circle at top right, #111a2e, #0a0e17);
            color: var(--text-main);
            min-height: 100vh;
            padding: 32px 24px;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 32px;
            padding-bottom: 24px;
            border-bottom: 1px solid var(--border-color);
        }
        .title-group h1 {
            font-size: 26px;
            font-weight: 700;
            background: linear-gradient(90deg, var(--accent-cyan), var(--accent-blue));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 6px;
        }
        .title-group p {
            color: var(--text-muted);
            font-size: 14px;
        }
        .status-badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 8px 16px;
            background: rgba(0, 230, 118, 0.12);
            border: 1px solid rgba(0, 230, 118, 0.3);
            border-radius: 999px;
            color: var(--accent-green);
            font-size: 13px;
            font-weight: 600;
        }
        .status-dot {
            width: 8px;
            height: 8px;
            background: var(--accent-green);
            border-radius: 50%;
            box-shadow: 0 0 8px var(--accent-green);
        }
        .kpi-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 20px;
            margin-bottom: 32px;
        }
        .kpi-card {
            background: var(--bg-card);
            backdrop-filter: blur(12px);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 24px;
            position: relative;
            overflow: hidden;
            transition: transform 0.2s ease, border-color 0.2s ease;
        }
        .kpi-card:hover {
            transform: translateY(-2px);
            border-color: rgba(255, 255, 255, 0.2);
        }
        .kpi-label {
            font-size: 13px;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 12px;
            display: flex;
            justify-content: space-between;
        }
        .kpi-value {
            font-size: 32px;
            font-weight: 700;
            margin-bottom: 8px;
        }
        .kpi-sub {
            font-size: 13px;
            color: var(--text-muted);
        }
        .val-cyan { color: var(--accent-cyan); }
        .val-blue { color: var(--accent-blue); }
        .val-green { color: var(--accent-green); }
        .val-purple { color: #d8b4fe; }

        .section-box {
            background: var(--bg-card);
            backdrop-filter: blur(12px);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 24px;
            margin-bottom: 24px;
        }
        .section-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }
        .section-header h2 {
            font-size: 18px;
            font-weight: 600;
        }
        .btn-test {
            background: linear-gradient(135deg, #00f2fe, #4facfe);
            color: #000;
            font-weight: 600;
            font-size: 14px;
            padding: 10px 20px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            transition: opacity 0.2s ease, transform 0.1s ease;
            display: inline-flex;
            align-items: center;
            gap: 8px;
        }
        .btn-test:hover {
            opacity: 0.9;
            transform: scale(1.02);
        }
        table {
            width: 100%;
            border-collapse: collapse;
            font-size: 14px;
        }
        th, td {
            padding: 14px 16px;
            text-align: left;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }
        th {
            color: var(--text-muted);
            font-weight: 500;
            font-size: 12px;
            text-transform: uppercase;
        }
        tr:hover {
            background: rgba(255, 255, 255, 0.02);
        }
        .badge {
            display: inline-block;
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
        }
        .badge-live {
            background: rgba(0, 230, 118, 0.15);
            color: #00e676;
        }
        .badge-sim {
            background: rgba(148, 163, 184, 0.15);
            color: #94a3b8;
        }
        .text-right {
            text-align: right;
        }
        .footer {
            margin-top: 40px;
            text-align: center;
            color: var(--text-muted);
            font-size: 13px;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="title-group">
                <h1>⚡ VibeSaver.ai — 50% 반값 바이브 코딩 에이전트 양판점</h1>
                <p>AST 시맨틱 델타 압축 & KV 캐시 90% 할인을 통한 토큰 차익(Arbitrage) 실시간 모니터링</p>
            </div>
            <div style="display: flex; align-items: center; gap: 12px;">
                <a href="/agent-window" style="background: linear-gradient(135deg, #00f2fe, #4facfe); color: #0a0d14; padding: 8px 16px; border-radius: 8px; font-weight: 700; text-decoration: none; font-size: 14px;">🖥️ 에이전트 윈도우 열기</a>
                <span class="status-badge">
                    <span class="status-dot"></span>
                    VibeSaver Online
                </span>
            </div>
        </header>


        <!-- KPI 4개 Grid -->
        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-label"><span>일반 상용 API 표준 요금</span></div>
                <div class="kpi-value val-cyan" id="kpi-standard">$0.0000</div>
                <div class="kpi-sub">기존 Cursor / 날 것 사용 시 100% 요금</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label"><span>사용자 청구 요금 (50% 할인!)</span></div>
                <div class="kpi-value val-blue" id="kpi-billed">$0.0000</div>
                <div class="kpi-sub">사용자가 감동하는 파격적인 50% 반값 요금</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label"><span>우리 실제 API 결제 원가</span></div>
                <div class="kpi-value val-green" id="kpi-actual">$0.0000</div>
                <div class="kpi-sub">KV 캐시 90% 할인 + 델타 압축 원가</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label"><span>순수 토큰 마진 수익 (Arbitrage)</span></div>
                <div class="kpi-value val-purple" id="kpi-margin">$0.0000</div>
                <div class="kpi-sub" id="kpi-margin-pct">평균 마진율: 0.0%</div>
            </div>
        </div>

        <!-- 실시간 차트 및 요청 테스트 영역 -->
        <div class="section-box">
            <div class="section-header">
                <h2>📊 실시간 요청 모니터링 로그 (Live Transactions)</h2>
                <button class="btn-test" onclick="sendTestRequest()">
                    🚀 Gemini Flash 시뮬레이션 요청 보내기
                </button>
            </div>
            <div style="overflow-x: auto;">
                <table>
                    <thead>
                        <tr>
                            <th>시간 (Timestamp)</th>
                            <th>모델 (Model)</th>
                            <th>호출 상태</th>
                            <th>입력 토큰 (Layer1 캐시 / dynamic)</th>
                            <th>출력 토큰</th>
                            <th class="text-right">표준 상용 요금</th>
                            <th class="text-right">사용자 청구액 (50%)</th>
                            <th class="text-right">실제 API 원가</th>
                            <th class="text-right">우리 수익 (마진율)</th>
                        </tr>
                    </thead>
                    <tbody id="history-table-body">
                        <tr>
                            <td colspan="9" style="text-align: center; color: var(--text-muted); padding: 24px;">
                                아직 기록된 API 호출이 없습니다. 상단의 'Gemini Flash 시뮬레이션 요청 보내기' 버튼을 눌러보세요!
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <div class="footer">
            <p>Smart Token-Saving Agent Gateway • Powered by Layered KV Caching & Semantic Delta Engine</p>
        </div>
    </div>

    <script>
        async function fetchSummary() {
            try {
                const res = await fetch("/v1/metrics/summary");
                const data = await res.json();
                document.getElementById("kpi-standard").innerText = "$" + data.total_standard_cost_usd.toFixed(4);
                document.getElementById("kpi-billed").innerText = "$" + data.total_user_billed_usd.toFixed(4);
                document.getElementById("kpi-actual").innerText = "$" + data.total_actual_api_cost_usd.toFixed(4);
                document.getElementById("kpi-margin").innerText = "$" + data.total_gross_margin_usd.toFixed(4);
                document.getElementById("kpi-margin-pct").innerText = `평균 마진율: ${data.overall_margin_percentage}% (총 ${data.total_requests}건)`;
            } catch (err) {
                console.error("Summary load err:", err);
            }
        }

        async function fetchHistory() {
            try {
                const res = await fetch("/v1/metrics/history");
                const data = await res.json();
                const tbody = document.getElementById("history-table-body");
                if (!data || data.length === 0) return;
                
                tbody.innerHTML = data.map(row => `
                    <tr>
                        <td>${row.timestamp}</td>
                        <td><strong>${row.model}</strong></td>
                        <td>
                            <span class="badge ${row.is_live_gemini ? 'badge-live' : 'badge-sim'}">
                                ${row.is_live_gemini ? '🟢 Gemini API 실시간' : '🔵 Delta 캐시 시뮬레이션'}
                            </span>
                        </td>
                        <td>${row.total_input_tokens} <small style="color:var(--text-muted)">(${row.cached_static_tokens} 캐시)</small></td>
                        <td>${row.output_tokens}</td>
                        <td class="text-right">$${row.standard_cost_usd.toFixed(5)}</td>
                        <td class="text-right" style="color: var(--accent-blue)">$${row.user_billed_usd.toFixed(5)}</td>
                        <td class="text-right" style="color: var(--accent-green)">$${row.actual_cost_usd.toFixed(5)}</td>
                        <td class="text-right" style="color: #d8b4fe; font-weight:700;">
                            +$${row.gross_margin_usd.toFixed(5)} (${row.margin_pct}%)
                        </td>
                    </tr>
                `).join('');
            } catch (err) {
                console.error("History load err:", err);
            }
        }

        async function sendTestRequest() {
            const samplePrompt = "바이브 코딩으로 로그인 기능을 붙여줘. 전체 코드를 다시 내보내지 말고 최소 Diff 델타 패치로 작성해줘.";
            try {
                const res = await fetch("/v1/chat/completions", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        model: "gemini-1.5-flash",
                        messages: [
                            { role: "system", content: "You are Smart Token-Saving Coding Agent. Always respond in diff patch." },
                            { role: "user", content: samplePrompt }
                        ],
                        max_tokens: 1500
                    })
                });
                await res.json();
                await refreshAll();
            } catch (err) {
                alert("테스트 요청 실패: " + err);
            }
        }

        async function refreshAll() {
            await fetchSummary();
            await fetchHistory();
        }

        // 2초마다 자동 갱신
        setInterval(refreshAll, 2000);
        refreshAll();
    </script>
</body>
</html>
"""
