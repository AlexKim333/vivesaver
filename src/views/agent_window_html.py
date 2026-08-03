"""
VibeSaver.ai - 에이전트 윈도우(Agent Window) UI 프로토타입 템플릿
- 2026 Ultra-Premium Dark Glassmorphism & Neon Cyan/Violet Accents
- WASM Delta 전처리 스테이터스, SHA-256 싱크 무결성 표시, Cache TTL 타이머
- 원클릭 [Apply Delta Patch] Diff 반영 및 실시간 50% 반값 절약 미터기 시연
"""

def get_agent_window_html() -> str:
    return """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VibeSaver.ai — 50% 반값 바이브 코딩 에이전트 윈도우</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600&family=Inter:wght@400;500;600;700&family=Outfit:wght@500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-obsidian: #0A0D14;
            --bg-glass: rgba(18, 24, 38, 0.75);
            --bg-glass-card: rgba(28, 36, 56, 0.65);
            --border-glass: rgba(0, 242, 254, 0.25);
            --border-highlight: rgba(0, 242, 254, 0.6);
            --cyan-glow: #00F2FE;
            --violet-glow: #9D4EDD;
            --emerald: #10B981;
            --amber: #F59E0B;
            --rose: #F43F5E;
            --text-main: #F8FAFC;
            --text-muted: #94A3B8;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-obsidian);
            color: var(--text-main);
            min-height: 100vh;
            overflow-x: hidden;
            background-image: 
                radial-gradient(circle at 15% 20%, rgba(0, 242, 254, 0.12) 0%, transparent 45%),
                radial-gradient(circle at 85% 80%, rgba(157, 78, 221, 0.12) 0%, transparent 45%);
            background-attachment: fixed;
            display: flex;
            flex-direction: column;
        }

        /* Top Header & Status Bar */
        header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0.85rem 2rem;
            background: rgba(10, 13, 20, 0.85);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid var(--border-glass);
            z-index: 100;
        }

        .brand-section {
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .brand-logo {
            font-family: 'Outfit', sans-serif;
            font-size: 1.4rem;
            font-weight: 800;
            background: linear-gradient(135deg, #00F2FE 0%, #4FACFE 50%, #9D4EDD 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: flex;
            align-items: center;
            gap: 0.4rem;
        }

        .brand-tag {
            font-size: 0.75rem;
            font-weight: 600;
            padding: 0.25rem 0.6rem;
            border-radius: 999px;
            background: rgba(0, 242, 254, 0.15);
            color: var(--cyan-glow);
            border: 1px solid rgba(0, 242, 254, 0.3);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .status-indicators {
            display: flex;
            align-items: center;
            gap: 0.8rem;
            flex-wrap: wrap;
        }

        .status-pill {
            display: flex;
            align-items: center;
            gap: 0.45rem;
            font-size: 0.8rem;
            font-weight: 600;
            padding: 0.35rem 0.8rem;
            border-radius: 8px;
            background: var(--bg-glass-card);
            border: 1px solid rgba(255, 255, 255, 0.08);
        }

        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            display: inline-block;
        }

        .dot-emerald { background: var(--emerald); box-shadow: 0 0 8px var(--emerald); }
        .dot-cyan { background: var(--cyan-glow); box-shadow: 0 0 8px var(--cyan-glow); }
        .dot-amber { background: var(--amber); box-shadow: 0 0 8px var(--amber); }

        .header-actions {
            display: flex;
            align-items: center;
            gap: 1rem;
        }

        .btn-nav {
            padding: 0.45rem 1rem;
            border-radius: 8px;
            font-size: 0.85rem;
            font-weight: 600;
            text-decoration: none;
            transition: all 0.25s ease;
            cursor: pointer;
            border: 1px solid rgba(255, 255, 255, 0.15);
            background: rgba(255, 255, 255, 0.05);
            color: var(--text-main);
        }

        .btn-nav:hover {
            border-color: var(--cyan-glow);
            background: rgba(0, 242, 254, 0.1);
            transform: translateY(-1px);
        }

        /* Main Workspace Split Layout */
        .workspace-grid {
            display: grid;
            grid-template-columns: 1.15fr 0.85fr;
            gap: 1.5rem;
            padding: 1.5rem 2rem;
            flex: 1;
            height: calc(100vh - 72px);
        }

        @media (max-width: 1024px) {
            .workspace-grid {
                grid-template-columns: 1fr;
                height: auto;
            }
        }

        /* Panel Glass Styles */
        .glass-panel {
            background: var(--bg-glass);
            backdrop-filter: blur(16px);
            border: 1px solid var(--border-glass);
            border-radius: 16px;
            display: flex;
            flex-direction: column;
            overflow: hidden;
            box-shadow: 0 12px 32px rgba(0, 0, 0, 0.35);
        }

        .panel-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0.9rem 1.25rem;
            background: rgba(28, 36, 56, 0.45);
            border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        }

        .panel-title {
            font-family: 'Outfit', sans-serif;
            font-size: 1rem;
            font-weight: 700;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        /* Left Column: File Tabs & Diff Viewer */
        .file-tabs {
            display: flex;
            gap: 0.5rem;
            padding: 0.6rem 1.25rem;
            background: rgba(15, 20, 32, 0.6);
            border-bottom: 1px solid rgba(255, 255, 255, 0.06);
            overflow-x: auto;
        }

        .file-tab {
            font-family: 'Fira Code', monospace;
            font-size: 0.82rem;
            padding: 0.4rem 0.9rem;
            border-radius: 6px;
            cursor: pointer;
            color: var(--text-muted);
            border: 1px solid transparent;
            background: transparent;
            transition: all 0.2s;
        }

        .file-tab.active {
            color: var(--cyan-glow);
            background: rgba(0, 242, 254, 0.12);
            border-color: rgba(0, 242, 254, 0.3);
            font-weight: 600;
        }

        .file-tab:hover:not(.active) {
            color: var(--text-main);
            background: rgba(255, 255, 255, 0.05);
        }

        .diff-workspace {
            flex: 1;
            padding: 1.25rem;
            overflow-y: auto;
            font-family: 'Fira Code', monospace;
            font-size: 0.88rem;
            line-height: 1.65;
            background: rgba(10, 13, 20, 0.75);
        }

        .diff-line {
            display: flex;
            padding: 0.15rem 0.5rem;
            border-radius: 4px;
            margin-bottom: 2px;
            white-space: pre-wrap;
        }

        .diff-line.add {
            background: rgba(16, 185, 129, 0.15);
            color: #6EE7B7;
            border-left: 3px solid var(--emerald);
        }

        .diff-line.del {
            background: rgba(244, 63, 94, 0.15);
            color: #FDA4AF;
            border-left: 3px solid var(--rose);
            text-decoration: line-through rgba(244, 63, 94, 0.5);
        }

        .diff-line.info {
            background: rgba(0, 242, 254, 0.12);
            color: var(--cyan-glow);
            font-weight: 600;
            border-left: 3px solid var(--cyan-glow);
        }

        .diff-line.neutral {
            color: var(--text-muted);
        }

        .line-num {
            width: 45px;
            color: rgba(148, 163, 184, 0.4);
            user-select: none;
            display: inline-block;
            text-align: right;
            margin-right: 15px;
        }

        /* Action Toolbar below Diff */
        .diff-toolbar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 1rem 1.25rem;
            background: rgba(28, 36, 56, 0.6);
            border-top: 1px solid rgba(255, 255, 255, 0.08);
        }

        .hash-badge {
            font-family: 'Fira Code', monospace;
            font-size: 0.8rem;
            color: var(--text-muted);
            display: flex;
            align-items: center;
            gap: 0.4rem;
        }

        .hash-badge span {
            color: var(--emerald);
            font-weight: 600;
        }

        .btn-apply-patch {
            background: linear-gradient(135deg, #00F2FE 0%, #4FACFE 100%);
            color: #0A0D14;
            font-family: 'Outfit', sans-serif;
            font-weight: 800;
            font-size: 0.95rem;
            padding: 0.65rem 1.5rem;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            box-shadow: 0 0 20px rgba(0, 242, 254, 0.4);
            transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .btn-apply-patch:hover {
            transform: translateY(-2px) scale(1.02);
            box-shadow: 0 0 30px rgba(0, 242, 254, 0.7);
        }

        /* Right Column: Vibe Coding Chat & Token Savings Meter */
        .chat-container {
            flex: 1;
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }

        .chat-history {
            flex: 1;
            padding: 1.25rem;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 1.25rem;
        }

        .message-bubble {
            max-width: 92%;
            padding: 1rem 1.15rem;
            border-radius: 14px;
            font-size: 0.93rem;
            line-height: 1.6;
        }

        .msg-user {
            align-self: flex-end;
            background: linear-gradient(135deg, rgba(0, 242, 254, 0.2) 0%, rgba(79, 172, 254, 0.25) 100%);
            border: 1px solid rgba(0, 242, 254, 0.4);
            border-bottom-right-radius: 4px;
        }

        .msg-agent {
            align-self: flex-start;
            background: rgba(28, 36, 56, 0.85);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-bottom-left-radius: 4px;
        }

        /* Token Economics Real-time Card */
        .token-econ-card {
            margin-top: 0.85rem;
            padding: 0.85rem 1rem;
            background: rgba(10, 13, 20, 0.85);
            border-radius: 10px;
            border: 1px solid rgba(0, 242, 254, 0.3);
        }

        .token-econ-title {
            font-size: 0.75rem;
            font-weight: 700;
            color: var(--cyan-glow);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 0.6rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .econ-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 0.6rem;
        }

        .econ-item {
            display: flex;
            flex-direction: column;
            background: rgba(255, 255, 255, 0.03);
            padding: 0.5rem;
            border-radius: 6px;
        }

        .econ-label {
            font-size: 0.72rem;
            color: var(--text-muted);
        }

        .econ-val {
            font-family: 'Fira Code', monospace;
            font-size: 0.95rem;
            font-weight: 700;
            margin-top: 0.2rem;
        }

        .val-saved { color: var(--cyan-glow); }
        .val-margin { color: var(--emerald); }

        /* Presets & Chat Input Bar */
        .chat-input-area {
            padding: 1rem 1.25rem;
            background: rgba(20, 26, 40, 0.8);
            border-top: 1px solid rgba(255, 255, 255, 0.08);
            display: flex;
            flex-direction: column;
            gap: 0.8rem;
        }

        .preset-buttons {
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
        }

        .btn-preset {
            font-size: 0.78rem;
            font-weight: 600;
            padding: 0.35rem 0.75rem;
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.05);
            color: var(--text-muted);
            border: 1px solid rgba(255, 255, 255, 0.12);
            cursor: pointer;
            transition: all 0.2s;
        }

        .btn-preset:hover {
            color: var(--cyan-glow);
            border-color: var(--cyan-glow);
            background: rgba(0, 242, 254, 0.1);
        }

        .input-row {
            display: flex;
            gap: 0.75rem;
        }

        .chat-input {
            flex: 1;
            background: rgba(10, 13, 20, 0.8);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 10px;
            padding: 0.75rem 1rem;
            color: var(--text-main);
            font-size: 0.92rem;
            font-family: 'Inter', sans-serif;
            outline: none;
            transition: border-color 0.2s;
        }

        .chat-input:focus {
            border-color: var(--cyan-glow);
            box-shadow: 0 0 12px rgba(0, 242, 254, 0.2);
        }

        .btn-send {
            background: var(--bg-glass-card);
            border: 1px solid var(--border-highlight);
            color: var(--cyan-glow);
            padding: 0 1.25rem;
            border-radius: 10px;
            font-weight: 700;
            cursor: pointer;
            transition: all 0.25s;
        }

        .btn-send:hover {
            background: rgba(0, 242, 254, 0.2);
            transform: scale(1.03);
        }

        /* Floating Toast */
        #toast {
            position: fixed;
            top: 24px;
            right: 24px;
            background: linear-gradient(135deg, rgba(16, 185, 129, 0.95), rgba(5, 150, 105, 0.95));
            color: #fff;
            padding: 1rem 1.5rem;
            border-radius: 12px;
            font-weight: 700;
            box-shadow: 0 10px 30px rgba(16, 185, 129, 0.4);
            display: flex;
            align-items: center;
            gap: 0.75rem;
            z-index: 1000;
            transform: translateY(-100px);
            opacity: 0;
            transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        }

        #toast.show {
            transform: translateY(0);
            opacity: 1;
        }

    </style>
</head>
<body>

    <!-- Floating Toast Notification -->
    <div id="toast">
        <span>🎉</span>
        <span id="toast-text">AST 델타 패치가 0.08초 만에 성공적으로 적용되었습니다! (토큰 50% 반값 절감)</span>
    </div>

    <!-- Top Status Bar -->
    <header>
        <div class="brand-section">
            <div class="brand-logo">
                <span>⚡ VibeSaver.ai</span>
            </div>
            <span class="brand-tag">50% 반값 바이브 코딩 에이전트 양판점</span>
        </div>

        <div class="status-indicators">
            <div class="status-pill">
                <span class="status-dot dot-cyan"></span>
                <span>WASM Delta Engine: READY</span>
            </div>
            <div class="status-pill">
                <span class="status-dot dot-emerald" id="sync-dot"></span>
                <span id="sync-status">SHA-256 State: IN-SYNC</span>
            </div>
            <div class="status-pill">
                <span class="status-dot dot-amber"></span>
                <span id="ttl-timer">Cache TTL: 298s WARM</span>
            </div>
            <div class="status-pill" style="border-color: rgba(16, 185, 129, 0.4);">
                <span style="color: var(--emerald); font-weight: 700;">💰 실시간 마진율: 60.0%</span>
            </div>
        </div>

        <div class="header-actions">
            <a href="/dashboard" class="btn-nav">📊 분석 대시보드</a>
            <a href="https://github.com/AlexKim333/vivesaver" target="_blank" class="btn-nav">🐙 GitHub Repo</a>
        </div>
    </header>

    <!-- Main Workspace Split Layout -->
    <main class="workspace-grid">
        
        <!-- Left Panel: Live Code & AST Delta Patch Workspace -->
        <section class="glass-panel">
            <div class="panel-header">
                <div class="panel-title">
                    <span>🖥️ AST 시맨틱 델타 패치 뷰어 (Diff Patch Workspace)</span>
                </div>
                <span style="font-size: 0.75rem; color: var(--text-muted);">Mode: Local WASM Preprocessor + Claude 3.5 Opus BYOK</span>
            </div>

            <div class="file-tabs">
                <div class="file-tab active" onclick="switchFile('billing', this)">src/services/erpnext_billing.py</div>
                <div class="file-tab" onclick="switchFile('moat', this)">src/services/moat_engine.py</div>
                <div class="file-tab" onclick="switchFile('delta', this)">src/services/delta_engine.py</div>
                <div class="file-tab" onclick="switchFile('local_wasm', this)" style="border-bottom: 2px solid var(--cyan-glow); color: var(--cyan-glow);">🧪 [WASM 로컬 델타 Sandbox]</div>
            </div>

            <div class="diff-workspace" id="diff-content">
<div class="diff-line info"><span class="line-num">1</span># [AST Delta Applied: Layer 1 Prefix Cached (90% 할인 영역 방어 완수)]</div>
<div class="diff-line neutral"><span class="line-num">14</span>class ERPNextBillingService:</div>
<div class="diff-line neutral"><span class="line-num">15</span>    def __init__(self, tenant_id: str):</div>
<div class="diff-line neutral"><span class="line-num">16</span>        self.tenant_id = tenant_id</div>
<div class="diff-line del"><span class="line-num">17</span>-       self.db_cursor = slow_query_all_unbilled_invoices()</div>
<div class="diff-line del"><span class="line-num">18</span>-       self.cache_ttl = None</div>
<div class="diff-line add"><span class="line-num">17</span>+       # 50% 반값 과금 및 60% 마진 화수분 엔진 탑재</div>
<div class="diff-line add"><span class="line-num">18</span>+       self.db_cursor = optimized_delta_invoices(limit=50, tenant_id=tenant_id)</div>
<div class="diff-line add"><span class="line-num">19</span>+       self.cache_ttl = 300 # Claude 3 Opus 공식 TTL(300초) Keep-Alive 방어</div>
<div class="diff-line neutral"><span class="line-num">20</span> </div>
<div class="diff-line neutral"><span class="line-num">21</span>    async def generate_half_price_invoice(self, tokens_used: int) -> dict:</div>
<div class="diff-line del"><span class="line-num">22</span>-       billed_cost = tokens_used * STANDARD_MARKET_RATE</div>
<div class="diff-line add"><span class="line-num">22</span>+       # 사용자에게는 무조건 시장가 대비 50% 반값 청구 (-50% SAVED)</div>
<div class="diff-line add"><span class="line-num">23</span>+       billed_cost = tokens_used * STANDARD_MARKET_RATE * 0.5</div>
<div class="diff-line add"><span class="line-num">24</span>+       actual_cost = self.calculate_cached_delta_cost(tokens_used)</div>
<div class="diff-line add"><span class="line-num">25</span>+       return {"billed": billed_cost, "margin_percent": 60.0}</div>
            </div>

            <div class="diff-toolbar">
                <div class="hash-badge">
                    🔒 SHA-256 State Hash: <span id="file-hash">9f8a2b3c7d... (IN-SYNC)</span>
                </div>
                <button class="btn-apply-patch" onclick="applyDeltaPatch()">
                    <span>⚡ APPLY DELTA PATCH</span>
                    <span style="font-size: 0.78rem; opacity: 0.85;">(0.08s)</span>
                </button>
            </div>
        </section>

        <!-- Right Panel: Vibe Coding Chat & Real-Time Token Economics Meter -->
        <section class="glass-panel">
            <div class="panel-header">
                <div class="panel-title">
                    <span>💬 바이브 코딩 채팅 & 경제성 미터기</span>
                </div>
                <span style="font-size: 0.75rem; color: var(--cyan-glow); font-weight: 700;">BYOK ENABLED</span>
            </div>

            <div class="chat-container">
                <div class="chat-history" id="chat-box">
                    <!-- Initial Chat Messages -->
                    <div class="message-bubble msg-user">
                        "WMS v2 ERPNext 결제 로직에 중복 쿼리 제거하고 성능 3배 개선 델타 패치 생성해줘!"
                    </div>

                    <div class="message-bubble msg-agent">
                        <strong>⚡ VibeSaver.ai 에이전트:</strong><br>
                        AST 시맨틱 델타 엔진이 불필요한 장황어를 정제하고, 90% 할인이 적용되는 Layer 1 캐시 영역을 방어하여 최소 Diff 패치를 생성했습니다! 좌측 뷰어에서 확인하세요.
                        
                        <!-- Embedded Token Economics Card -->
                        <div class="token-econ-card">
                            <div class="token-econ-title">
                                <span>💰 이번 질의 토큰 경제성 분석</span>
                                <span style="color: var(--emerald);">VIBE SAVED</span>
                            </div>
                            <div class="econ-grid">
                                <div class="econ-item">
                                    <span class="econ-label">표준 정가 (Market Rate)</span>
                                    <span class="econ-val">$0.0800</span>
                                </div>
                                <div class="econ-item">
                                    <span class="econ-label">바이브 반값 청구 (-50%)</span>
                                    <span class="econ-val val-saved">$0.0400</span>
                                </div>
                                <div class="econ-item">
                                    <span class="econ-label">실제 API 원가 (Cache Hit)</span>
                                    <span class="econ-val">$0.0160</span>
                                </div>
                                <div class="econ-item">
                                    <span class="econ-label">우리 양판점 수익 (Margin)</span>
                                    <span class="econ-val val-margin">+$0.0240 (60.0%)</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Chat Input Area with Presets -->
                <div class="chat-input-area">
                    <div class="preset-buttons">
                        <button class="btn-preset" onclick="runPreset('🚀 WMS v2 결제 로직 델타 생성')">🚀 WMS v2 결제 델타</button>
                        <button class="btn-preset" onclick="runPreset('🔍 SHA-256 무결성 검증 시연')">🔍 SHA-256 싱크 검증</button>
                        <button class="btn-preset" onclick="runPreset('🔥 캐시 킵얼라이브 하트비트 시동')">🔥 캐시 TTL 유지</button>
                    </div>
                    <div class="input-row">
                        <input type="text" id="user-input" class="chat-input" placeholder="말하는 대로 코딩하는 바이브 코딩 입력 (예: '오타 잡고 성능 최적화해줘')...">
                        <button class="btn-send" onclick="sendVibeMessage()">전송 ⚡</button>
                    </div>
                </div>
            </div>
        </section>

    </main>

    <script>
        // Cache TTL Timer Countdown Simulation
        let ttlSeconds = 298;
        setInterval(() => {
            if (ttlSeconds > 0) {
                ttlSeconds--;
                document.getElementById('ttl-timer').innerText = `Cache TTL: ${ttlSeconds}s WARM`;
                if (ttlSeconds <= 45) {
                    document.getElementById('ttl-timer').innerText = `Cache TTL: ${ttlSeconds}s (KEEP-ALIVE PING!)`;
                    document.getElementById('ttl-timer').style.color = 'var(--rose)';
                }
            } else {
                ttlSeconds = 300; // Reset after automated Keep-Alive ping
            }
        }, 1000);

        // Apply Delta Patch Simulation
        function applyDeltaPatch() {
            const toast = document.getElementById('toast');
            toast.classList.add('show');
            setTimeout(() => {
                toast.classList.remove('show');
            }, 3800);

            // Update SHA-256 hash to a newly applied synced hash
            document.getElementById('file-hash').innerText = "a1b2c3d4e5... (VALIDATED & IN-SYNC)";
            document.getElementById('file-hash').style.color = "var(--emerald)";
        }

        // Preset & Chat Send Simulation
        function runPreset(text) {
            document.getElementById('user-input').value = text;
            sendVibeMessage();
        }

        function sendVibeMessage() {
            const inputEl = document.getElementById('user-input');
            const text = inputEl.value.trim();
            if (!text) return;

            const chatBox = document.getElementById('chat-box');
            
            // Append User Message
            const userDiv = document.createElement('div');
            userDiv.className = 'message-bubble msg-user';
            userDiv.innerText = text;
            chatBox.appendChild(userDiv);

            inputEl.value = '';
            chatBox.scrollTop = chatBox.scrollHeight;

            // Simulate Agent Response
            setTimeout(() => {
                const agentDiv = document.createElement('div');
                agentDiv.className = 'message-bubble msg-agent';
                agentDiv.innerHTML = `
                    <strong>⚡ VibeSaver.ai 에이전트:</strong><br>
                    WASM 델타 엔진이 요청을 실시간 전처리하고, SHA-256 무결성을 검증한 뒤 <strong>50% 반값 요금</strong>으로 코딩 패치를 완료했습니다!
                    <div class="token-econ-card">
                        <div class="token-econ-title">
                            <span>💰 실시간 토큰 절약 분석</span>
                            <span style="color: var(--emerald);">50% HALF PRICE</span>
                        </div>
                        <div class="econ-grid">
                            <div class="econ-item">
                                <span class="econ-label">표준 정가 (Market Rate)</span>
                                <span class="econ-val">$0.0620</span>
                            </div>
                            <div class="econ-item">
                                <span class="econ-label">바이브 반값 청구 (-50%)</span>
                                <span class="econ-val val-saved">$0.0310</span>
                            </div>
                            <div class="econ-item">
                                <span class="econ-label">실제 API 원가 (Cache Hit)</span>
                                <span class="econ-val">$0.0124</span>
                            </div>
                            <div class="econ-item">
                                <span class="econ-label">우리 양판점 수익 (Margin)</span>
                                <span class="econ-val val-margin">+$0.0186 (60.0%)</span>
                            </div>
                        </div>
                    </div>
                `;
                chatBox.appendChild(agentDiv);
                chatBox.scrollTop = chatBox.scrollHeight;
            }, 600);
        }

        // File Switcher Simulation
        function switchFile(fileKey, tabEl) {
            document.querySelectorAll('.file-tab').forEach(t => t.classList.remove('active'));
            tabEl.classList.add('active');
            
            const diffContent = document.getElementById('diff-content');
            if (fileKey === 'moat') {
                diffContent.innerHTML = `
<div class="diff-line info"><span class="line-num">1</span># [Moat Engine: Warm Cache & Layered Context Lock-in]</div>
<div class="diff-line neutral"><span class="line-num">10</span>class MoatEngineService:</div>
<div class="diff-line del"><span class="line-num">11</span>-       def evict_cache_after_timeout():</div>
<div class="diff-line add"><span class="line-num">11</span>+       def keepalive_warm_cache(tenant_id: str):</div>
<div class="diff-line add"><span class="line-num">12</span>+           # 캐시 TTL 30초 전 1토큰 하트비트 핑 발송으로 90% 할인 영구 유지</div>
<div class="diff-line add"><span class="line-num">13</span>+           return send_dummy_ping(tenant_id)</div>
                `;
                document.getElementById('file-hash').innerText = "c4a1e90b2f... (IN-SYNC)";
            } else if (fileKey === 'delta') {
                diffContent.innerHTML = `
<div class="diff-line info"><span class="line-num">1</span># [Delta Engine: SHA-256 State Verification & Force Refresh]</div>
<div class="diff-line neutral"><span class="line-num">15</span>    def verify_and_update_state(self, filepath, content, expected_hash):</div>
<div class="diff-line del"><span class="line-num">16</span>-       return True</div>
<div class="diff-line add"><span class="line-num">16</span>+       actual = self.compute_state_hash(content)</div>
<div class="diff-line add"><span class="line-num">17</span>+       if expected_hash and expected_hash != actual:</div>
<div class="diff-line add"><span class="line-num">18</span>+           return False, actual, True # Out-of-Sync 자동 보정</div>
                `;
                document.getElementById('file-hash').innerText = "7b2d18ef4a... (IN-SYNC)";
            } else if (fileKey === 'local_wasm') {
                diffContent.innerHTML = `
<div style="padding: 1rem; display: flex; flex-direction: column; gap: 1rem; color: #fff;">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <span style="color: var(--cyan-glow); font-weight: 700; font-size: 0.9rem;">⚡ 로컬 WASM/JS 델타 전처리기 & SHA-256 무결성 검증기 (Client-Side Zero-Cost Engine)</span>
        <button onclick="executeLocalWasmDelta()" style="background: linear-gradient(135deg, #00f2fe, #4facfe); color: #0a0d14; border: none; padding: 6px 14px; border-radius: 6px; font-weight: 700; cursor: pointer; font-size: 0.8rem;">⚡ 실시간 델타 압축 수행</button>
    </div>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1rem;">
        <div>
            <div style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 4px;">원본 코드 (Original Code / Base State)</div>
            <textarea id="wasm-old-code" style="width: 100%; height: 110px; background: rgba(0,0,0,0.4); border: 1px solid rgba(255,255,255,0.2); border-radius: 6px; color: #fff; font-family: monospace; padding: 8px; font-size: 0.8rem;">def calculate_price(tokens):
    # 기존 상용 정가 API 호출 방식
    return tokens * 0.0800</textarea>
        </div>
        <div>
            <div style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 4px;">수정 대상 코드 (Modified Code / Vibe Target)</div>
            <textarea id="wasm-new-code" style="width: 100%; height: 110px; background: rgba(0,0,0,0.4); border: 1px solid rgba(0,242,254,0.4); border-radius: 6px; color: #fff; font-family: monospace; padding: 8px; font-size: 0.8rem;">def calculate_price(tokens):
    # VibeSaver 50% 반값 + 60% 마진 화수분 엔진 적용
    billed = tokens * 0.0800 * 0.5
    return billed</textarea>
        </div>
    </div>
    <div id="wasm-output-area" style="background: rgba(0,0,0,0.5); border: 1px dashed var(--cyan-glow); border-radius: 8px; padding: 12px; font-family: monospace; font-size: 0.82rem;">
        <div style="color: var(--text-muted);">[위 '⚡ 실시간 델타 압축 수행' 버튼을 누르면 브라우저 네이티브 JS/WASM 모듈이 0.01초 만에 SHA-256 해시와 델타 Diff 토큰 절약률을 계산합니다]</div>
    </div>
</div>
                `;
                document.getElementById('file-hash').innerText = "WASM LOCAL SANDBOX (READY)";
            } else {
                diffContent.innerHTML = `
<div class="diff-line info"><span class="line-num">1</span># [AST Delta Applied: Layer 1 Prefix Cached (90% 할인 영역 방어 완수)]</div>
<div class="diff-line neutral"><span class="line-num">14</span>class ERPNextBillingService:</div>
<div class="diff-line neutral"><span class="line-num">15</span>    def __init__(self, tenant_id: str):</div>
<div class="diff-line neutral"><span class="line-num">16</span>        self.tenant_id = tenant_id</div>
<div class="diff-line del"><span class="line-num">17</span>-       self.db_cursor = slow_query_all_unbilled_invoices()</div>
<div class="diff-line add"><span class="line-num">17</span>+       # 50% 반값 과금 및 60% 마진 화수분 엔진 탑재</div>
<div class="diff-line add"><span class="line-num">18</span>+       self.db_cursor = optimized_delta_invoices(limit=50, tenant_id=tenant_id)</div>
                `;
                document.getElementById('file-hash').innerText = "9f8a2b3c7d... (IN-SYNC)";
            }
        }

        async function computeSHA256Hash(text) {
            const msgBuffer = new TextEncoder().encode(text);
            const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
            const hashArray = Array.from(new Uint8Array(hashBuffer));
            return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
        }

        async function executeLocalWasmDelta() {
            const oldCode = document.getElementById('wasm-old-code').value;
            const newCode = document.getElementById('wasm-new-code').value;
            
            const oldHash = await computeSHA256Hash(oldCode);
            const newHash = await computeSHA256Hash(newCode);
            
            const oldLines = oldCode.split('\n');
            const newLines = newCode.split('\n');
            
            let diffHtml = '';
            let deltaTokenCount = 0;
            const oldTokenCount = Math.max(1, Math.ceil(oldCode.length / 4));
            
            newLines.forEach((line, idx) => {
                if (oldLines[idx] !== line) {
                    diffHtml += `<div class="diff-line add" style="padding: 2px 6px;"><span class="line-num">${idx+1}</span>+ ${line}</div>`;
                    deltaTokenCount += Math.ceil(line.length / 4);
                } else {
                    diffHtml += `<div class="diff-line neutral" style="padding: 2px 6px;"><span class="line-num">${idx+1}</span>  ${line}</div>`;
                }
            });
            
            const savedPct = Math.max(0, Math.round((1 - (deltaTokenCount / (oldTokenCount || 1))) * 100));
            
            document.getElementById('wasm-output-area').innerHTML = `
                <div style="margin-bottom: 8px; color: var(--emerald); font-weight: 700;">
                    ✅ [WASM 로컬 델타 추출 성공] SHA-256 해시 및 AST Diff 연산 완료 (0.01s)
                </div>
                <div style="font-size: 0.75rem; color: var(--text-muted); margin-bottom: 6px;">
                    🔒 원본 SHA-256: <span style="color: #fff;">${oldHash.substring(0, 16)}...</span> | 
                    ⚡ 변경 SHA-256: <span style="color: var(--cyan-glow);">${newHash.substring(0, 16)}...</span> (IN-SYNC)
                </div>
                <div style="font-size: 0.78rem; margin-bottom: 8px; color: #fff;">
                    📊 토큰 경제성 전처리 결과: 원본 <strong>${oldTokenCount} 토큰</strong> → 델타 전송 <strong>${deltaTokenCount} 토큰</strong> (<span style="color: var(--emerald); font-weight: 700;">-${savedPct}% 입력 토큰 절약 완수!</span>)
                </div>
                <div style="background: rgba(10,13,20,0.9); border-radius: 6px; padding: 6px; margin-bottom: 8px;">
                    ${diffHtml}
                </div>
                <button onclick="runPreset('🚀 WASM 델타 전송: -${savedPct}% 절감 패치 적용 요청')" style="background: var(--emerald); color: #000; border: none; padding: 6px 12px; border-radius: 6px; font-weight: 700; cursor: pointer; font-size: 0.75rem;">💬 이 델타 패치를 에이전트 채팅으로 전송 ⚡</button>
            `;
            document.getElementById('file-hash').innerText = `${newHash.substring(0, 10)}... (WASM VERIFIED)`;
        }
    </script>
</body>
</html>"""
