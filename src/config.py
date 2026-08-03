import os
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

class PricingModel(BaseModel):
    """
    단위: USD per 1 Million Tokens (100만 토큰당 달러 가격)
    Anthropic / Google 표준 상용 단가 기준
    """
    model_name: str
    standard_input_price: float   # 표준 입력 단가 ($/1M tokens)
    cached_input_price: float     # KV 캐시 읽기 단가 (할인 적용)
    standard_output_price: float  # 표준 출력 단가 ($/1M tokens)


# 모델별 상용 API 단가 표 (Claude 3.5 Sonnet / Opus 및 Gemini Flash 시리즈)
MODEL_PRICING_CATALOG = {
    "claude-3-5-sonnet": PricingModel(
        model_name="claude-3-5-sonnet",
        standard_input_price=3.00,
        cached_input_price=0.30,   # 90% 할인 적용
        standard_output_price=15.00
    ),
    "claude-3-opus": PricingModel(
        model_name="claude-3-opus",
        standard_input_price=15.00,
        cached_input_price=1.50,   # 90% 할인 적용
        standard_output_price=75.00
    ),
    "gemini-1.5-flash": PricingModel(
        model_name="gemini-1.5-flash",
        standard_input_price=0.075,
        cached_input_price=0.01875,  # 75% 캐시 읽기 할인
        standard_output_price=0.30
    ),
    "gemini-2.0-flash": PricingModel(
        model_name="gemini-2.0-flash",
        standard_input_price=0.075,
        cached_input_price=0.01875,  # 75% 캐시 읽기 할인
        standard_output_price=0.30
    ),
    "gemini-3.6-flash": PricingModel(
        model_name="gemini-3.6-flash",
        standard_input_price=0.075,
        cached_input_price=0.01875,  # 75% 캐시 읽기 할인
        standard_output_price=0.30
    ),
    "gemini-flash": PricingModel(
        model_name="gemini-flash",
        standard_input_price=0.075,
        cached_input_price=0.01875,
        standard_output_price=0.30
    )
}

# 비즈니스 수익 마진 및 할인 정책 설정
USER_DISCOUNT_RATE = 0.50  # 사용자에게 50% 파격 할인 혜택 제공 (표준 단가의 50%만 청구)
CACHE_READ_RATIO = 0.85    # 우리 엔진을 통과할 때 전체 입력 토큰 중 Layer 1(캐시) 비율 목표 (85%)
DELTA_OUTPUT_RATIO = 0.20  # 전체 출력 중 패치 델타로 줄어드는 비율 (원본 100% 중 20% 토큰만 사용)

class GatewayConfig:
    PORT: int = int(os.getenv("PORT", 8080))
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    DEFAULT_MODEL: str = "gemini-1.5-flash"
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

config = GatewayConfig()

