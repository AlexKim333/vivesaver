import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from src.config import config
from src.models.gateway_models import ChatCompletionRequest, ChatCompletionResponse
from src.services.proxy_router import proxy_router
from src.services.cache_manager import cache_manager
from src.services.delta_engine import delta_engine
from src.services.metrics_store import metrics_store
from src.views.dashboard_html import DASHBOARD_HTML_TEMPLATE
from src.views.agent_window_html import get_agent_window_html

app = FastAPI(
    title="VibeSaver.ai — 토큰절약형 바이브 코딩 에이전트 양판점 게이트웨이",
    description="AST 시맨틱 델타 압축과 KV 캐시 90% 할인을 통해 사용자에게 50% 반값 이용 혜택을 제공하고 60% 차익 마진을 창출하는 AI 미들웨어",
    version="1.0.0-MVP"
)

@app.get("/")
async def root():
    return {
        "service": "VibeSaver.ai — Token-Saving Vibe Coding Agent Gateway",
        "status": "online",
        "philosophy": "Zero-Config Vibe Coding with 50% Billed Cost & 3x Speed",
        "agent_window_url": "/agent-window",
        "dashboard_url": "/dashboard",
        "documentation": "/docs"
    }


@app.get("/agent-window", response_class=HTMLResponse)
async def agent_window_view():
    """
    VibeSaver.ai - 50% 반값 바이브 코딩 에이전트 윈도우 UI 프로토타입
    """
    return HTMLResponse(content=get_agent_window_html(), status_code=200)


@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_view():
    """
    실시간 토큰 절약량, 마진율 및 통계 히스토리 시각화 웹 대시보드
    """
    return HTMLResponse(content=DASHBOARD_HTML_TEMPLATE, status_code=200)


@app.get("/v1/metrics/summary")
async def get_metrics_summary():
    """
    전체 요청 통계, 총 절감액 및 차익 수익 마진 요약 반환
    """
    return metrics_store.get_summary()

@app.get("/v1/metrics/history")
async def get_metrics_history():
    """
    최근 API 트랜잭션 기록 목록 반환
    """
    return metrics_store.history

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "cache_hits": cache_manager.cache_hits,
        "cache_evictions": cache_manager.cache_evictions,
        "cache_status": cache_manager.get_cache_status("gemini-1.5-flash"),
        "delta_optimizations": delta_engine.optimized_turns,
        "delta_sync_status": delta_engine.get_sync_status(),
        "total_requests": metrics_store.total_requests
    }



@app.post("/v1/chat/completions", response_model=ChatCompletionResponse)
async def chat_completions(req: ChatCompletionRequest):
    """
    Cursor IDE 또는 AI 양판점 앱 호환 API 엔드포인트:
    - 사용자 프롬프트를 수신하여 Layer 1 (KV캐시) 및 Layer 2 (델타 Diff)로 분할
    - 50% 사용자 할인 적용 및 우리의 토큰 차익(Arbitrage) 리포트 포함 반환
    """
    try:
        response = await proxy_router.process_chat_completion(req)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Proxy Gateway Error: {str(e)}")

if __name__ == "__main__":
    print("=" * 60)
    print(" 🚀 VibeSaver.ai — 50% 반값 바이브 코딩 에이전트 양판점 게이트웨이 시작")
    print(f" 📡 포트: {config.PORT} | 기본 모델: {config.DEFAULT_MODEL}")
    print(f" 📊 실시간 모니터링 대시보드: http://localhost:{config.PORT}/dashboard")
    print("=" * 60)
    uvicorn.run("main:app", host="0.0.0.0", port=config.PORT, reload=config.DEBUG)


