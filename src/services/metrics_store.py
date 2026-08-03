import time
from typing import List, Dict, Any
from src.models.gateway_models import TokenEconomicsReport

class RealtimeMetricsStore:
    """
    실시간 토큰 절약량 및 비즈니스 차익 마진 모니터링 저장소 (In-Memory MVP)
    """
    def __init__(self):
        self.history: List[Dict[str, Any]] = []
        self.total_requests: int = 0
        self.total_input_tokens_saved: int = 0
        self.total_output_tokens_saved: int = 0
        
        # 누적 금액 통계 (USD)
        self.total_standard_cost_usd: float = 0.0      # 표준 상용 API 사용 시 총 요금
        self.total_user_billed_usd: float = 0.0        # 사용자 청구 총 요금 (50% 할인 혜택 제공)
        self.total_actual_api_cost_usd: float = 0.0    # 우리 서버의 실제 API 결제 원가
        self.total_gross_margin_usd: float = 0.0       # 누적 토큰 차익 수익

    def record_transaction(self, report: TokenEconomicsReport, is_live_gemini: bool = False):
        self.total_requests += 1
        
        # 캐시 및 델타 패치로 절약된 토큰 수
        self.total_input_tokens_saved += report.cached_static_tokens
        self.total_output_tokens_saved += int(report.output_tokens * 4)  # 패치 대비 전체 재출력 추정 차이
        
        # 누적 비용 갱신
        self.total_standard_cost_usd = round(self.total_standard_cost_usd + report.standard_market_cost_usd, 6)
        self.total_user_billed_usd = round(self.total_user_billed_usd + report.user_billed_cost_usd, 6)
        self.total_actual_api_cost_usd = round(self.total_actual_api_cost_usd + report.actual_api_cost_usd, 6)
        self.total_gross_margin_usd = round(self.total_gross_margin_usd + report.gross_margin_usd, 6)
        
        # 히스토리 기록
        record = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "model": report.model_used,
            "is_live_gemini": is_live_gemini,
            "total_input_tokens": report.total_input_tokens,
            "cached_static_tokens": report.cached_static_tokens,
            "delta_dynamic_tokens": report.delta_dynamic_tokens,
            "output_tokens": report.output_tokens,
            "standard_cost_usd": report.standard_market_cost_usd,
            "user_billed_usd": report.user_billed_cost_usd,
            "actual_cost_usd": report.actual_api_cost_usd,
            "gross_margin_usd": report.gross_margin_usd,
            "margin_pct": report.gross_margin_percentage
        }
        self.history.insert(0, record)  # 최신 요청이 위로 오도록 삽입
        if len(self.history) > 100:
            self.history.pop()

    def get_summary(self) -> Dict[str, Any]:
        overall_margin_pct = (
            round((self.total_gross_margin_usd / self.total_user_billed_usd) * 100.0, 2)
            if self.total_user_billed_usd > 0 else 0.0
        )
        return {
            "total_requests": self.total_requests,
            "total_input_tokens_saved": self.total_input_tokens_saved,
            "total_output_tokens_saved": self.total_output_tokens_saved,
            "total_standard_cost_usd": self.total_standard_cost_usd,
            "total_user_billed_usd": self.total_user_billed_usd,
            "total_actual_api_cost_usd": self.total_actual_api_cost_usd,
            "total_gross_margin_usd": self.total_gross_margin_usd,
            "overall_margin_percentage": overall_margin_pct,
            "history_count": len(self.history)
        }

metrics_store = RealtimeMetricsStore()
