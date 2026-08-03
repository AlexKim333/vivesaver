from src.config import MODEL_PRICING_CATALOG, USER_DISCOUNT_RATE, DELTA_OUTPUT_RATIO
from src.models.gateway_models import TokenEconomicsReport

def calculate_token_economics(
    model_name: str,
    total_input_tokens: int,
    cached_static_tokens: int,
    delta_dynamic_tokens: int,
    output_tokens: int
) -> TokenEconomicsReport:
    """
    토큰 단가 및 비즈니스 마진(Token Arbitrage)을 계산하는 핵심 유틸리티
    """
    pricing = MODEL_PRICING_CATALOG.get(model_name, MODEL_PRICING_CATALOG["claude-3-5-sonnet"])
    
    # 1. 일반 Cursor / 상용 에이전트를 그냥 썼을 때의 원가 (100% standard cost)
    # 우리 델타 패치 엔진이 없을 경우 전체 파일을 재출력하므로 출력 토큰이 DELTA_OUTPUT_RATIO 만큼 큼
    standard_uncompressed_output = max(1, int(output_tokens / DELTA_OUTPUT_RATIO))
    standard_input_cost = (total_input_tokens / 1_000_000.0) * pricing.standard_input_price
    standard_output_cost = (standard_uncompressed_output / 1_000_000.0) * pricing.standard_output_price
    standard_market_cost_usd = round(standard_input_cost + standard_output_cost, 6)
    
    # 2. 사용자에게 청구하는 비용 (50% 할인 혜택 제공 - 마케팅 포인트!)
    user_billed_cost_usd = round(standard_market_cost_usd * (1.0 - USER_DISCOUNT_RATE), 6)
    
    # 3. 우리의 실제 API 원가 (KV캐시 읽기 90% 할인 + 델타 패치 출력 최소화)
    cached_cost = (cached_static_tokens / 1_000_000.0) * pricing.cached_input_price
    dynamic_cost = (delta_dynamic_tokens / 1_000_000.0) * pricing.standard_input_price
    actual_output_cost = (output_tokens / 1_000_000.0) * pricing.standard_output_price
    actual_api_cost_usd = round(cached_cost + dynamic_cost + actual_output_cost, 6)
    
    # 4. 토큰 마진 및 마진율 계산
    gross_margin_usd = round(user_billed_cost_usd - actual_api_cost_usd, 6)
    gross_margin_percentage = (
        round((gross_margin_usd / user_billed_cost_usd) * 100.0, 2)
        if user_billed_cost_usd > 0 else 0.0
    )
    
    return TokenEconomicsReport(
        model_used=model_name,
        total_input_tokens=total_input_tokens,
        cached_static_tokens=cached_static_tokens,
        delta_dynamic_tokens=delta_dynamic_tokens,
        output_tokens=output_tokens,
        standard_market_cost_usd=standard_market_cost_usd,
        user_billed_cost_usd=user_billed_cost_usd,
        actual_api_cost_usd=actual_api_cost_usd,
        gross_margin_usd=gross_margin_usd,
        gross_margin_percentage=gross_margin_percentage
    )

