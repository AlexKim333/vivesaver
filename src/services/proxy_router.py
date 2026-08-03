import uuid
from src.models.gateway_models import (
    ChatCompletionRequest,
    ChatCompletionResponse,
    ChatMessage,
    TokenEconomicsReport
)
from src.services.cache_manager import cache_manager
from src.services.delta_engine import delta_engine
from src.services.gemini_client import gemini_client
from src.services.metrics_store import metrics_store
from src.utils.token_estimator import calculate_token_economics

class ProxyRouterService:
    """
    Cursor / VSCode 요청을 가로채어 컨텍스트 캐싱 및 델타 패치로 최적화한 뒤
    Gemini Flash 실시간 API 또는 시뮬레이션 호출 후 마진 계산을 수행하는 핵심 서비스
    """
    async def process_chat_completion(self, req: ChatCompletionRequest) -> ChatCompletionResponse:
        # 1. 시맨틱 델타 엔진으로 불필요 공백 및 중복 메시지 정제
        compressed_messages = delta_engine.compress_input_messages(req.messages)
        
        # 2. 계층형 KV 캐시 관리자로 Static vs Dynamic 토큰 비율 분리 (모델별 공식 TTL 반영)
        total_tokens, cached_tokens, dynamic_tokens = cache_manager.analyze_token_split(compressed_messages, req.model)
        expected_output_tokens = delta_engine.estimate_patch_output_tokens(req.max_tokens or 1000)

        
        # 3. Gemini API 실시간 연동 시도 (모델명이 gemini이고 API키 존재 시)
        assistant_reply = ""
        is_live_gemini = False
        if "gemini" in req.model.lower():
            try:
                live_text, usage_meta = await gemini_client.generate_content(
                    messages=compressed_messages,
                    model_name=req.model
                )
                if live_text:
                    assistant_reply = live_text
                    is_live_gemini = True
                    if usage_meta:
                        total_tokens = usage_meta.get("promptTokenCount", total_tokens)
                        cached_tokens = usage_meta.get("cachedContentTokenCount", cached_tokens)
                        dynamic_tokens = max(0, total_tokens - cached_tokens)
                        expected_output_tokens = usage_meta.get("candidatesTokenCount", expected_output_tokens)
            except Exception as e:
                # API키 미입력 또는 오류 시 폴백 시뮬레이션으로 전환
                assistant_reply = f"[Gemini Fallback Simulation Mode: {str(e)}]\n"
        
        # 4. 토큰 경제성 및 차익(Arbitrage) 리포트 계산
        report: TokenEconomicsReport = calculate_token_economics(
            model_name=req.model,
            total_input_tokens=total_tokens,
            cached_static_tokens=cached_tokens,
            delta_dynamic_tokens=dynamic_tokens,
            output_tokens=expected_output_tokens
        )
        
        # 5. 실시간 통계 저장소에 트랜잭션 기록
        metrics_store.record_transaction(report, is_live_gemini=is_live_gemini)
        
        # 6. 시뮬레이션 응답 생성 (실제 API 응답이 없을 경우)
        if not assistant_reply:
            last_user_msg = "아무 질의"
            for m in reversed(compressed_messages):
                if m.role == "user":
                    last_user_msg = m.content[:50]
                    break
                    
            assistant_reply = (
                f"[Smart Proxy Optimization Applied - 50% Billed Discount!]\n"
                f"요청하신 작업('{last_user_msg}...')을 계층형 KV 캐시와 시맨틱 델타 패치로 처리했습니다.\n\n"
                f"```diff\n"
                f"--- target_file.py\n"
                f"+++ target_file.py (Optimized Delta Patch)\n"
                f"@@ -10,3 +10,5 @@\n"
                f"- # old implementation\n"
                f"+ # Token-Saving Gateway applied zero-config optimization\n"
                f"+ def execute_optimized_flow():\n"
                f"+     return True\n"
                f"```"
            )
        
        summary = (
            f"[{'🟢 LIVE GEMINI' if is_live_gemini else '🔵 SIMULATION'}] "
            f"표준 원가: ${report.standard_market_cost_usd:.5f} -> "
            f"사용자 청구(50% 할인): ${report.user_billed_cost_usd:.5f} | "
            f"실제 API 원가: ${report.actual_api_cost_usd:.5f} | "
            f"순수 토큰 차익 마진: ${report.gross_margin_usd:.5f} (마진율: {report.gross_margin_percentage}%)"
        )
        
        return ChatCompletionResponse(
            id=f"chatcmpl-saver-{uuid.uuid4().hex[:8]}",
            model=req.model,
            message=ChatMessage(role="assistant", content=assistant_reply),
            token_economics=report,
            optimization_summary=summary
        )

proxy_router = ProxyRouterService()

