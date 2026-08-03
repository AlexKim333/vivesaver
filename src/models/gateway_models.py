from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class ChatMessage(BaseModel):
    role: str  # "user", "assistant", "system"
    content: str

class ChatCompletionRequest(BaseModel):
    model: str = "claude-3-5-sonnet"
    messages: List[ChatMessage]
    temperature: Optional[float] = 0.2
    max_tokens: Optional[int] = 2048
    stream: Optional[bool] = False
    metadata: Optional[Dict[str, Any]] = None

class TokenEconomicsReport(BaseModel):
    """
    토큰 단가 및 비즈니스 마진 분석 결과 리포트
    """
    model_used: str
    total_input_tokens: int
    cached_static_tokens: int      # Layer 1 캐시로 처리된 토큰 수
    delta_dynamic_tokens: int      # Layer 2 델타로 처리된 토큰 수
    output_tokens: int             # Diff 패치 형태로 축소된 출력 토큰 수
    
    # 비용 비교 (USD)
    standard_market_cost_usd: float    # 일반 Cursor/Opus 사용 시 원래 비용 (100%)
    user_billed_cost_usd: float        # 사용자에게 청구하는 비용 (50% 할인 혜택 제공)
    actual_api_cost_usd: float         # 우리의 실제 Anthropic/Google API 원가 (KV캐시+델타 할인)
    
    # 비즈니스 수익
    gross_margin_usd: float            # 순수 토큰 차익 수익 (user_billed - actual_api)
    gross_margin_percentage: float     # 마진율 (%)

class ChatCompletionResponse(BaseModel):
    id: str
    model: str
    message: ChatMessage
    token_economics: TokenEconomicsReport
    optimization_summary: str
