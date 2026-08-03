import time
from typing import Tuple, List, Dict, Any
from src.models.gateway_models import ChatMessage
from src.config import CACHE_READ_RATIO

# 원청별 공식 프롬프트 캐시 유지 시간(TTL, 초 단위) 스펙 매핑
MODEL_TTL_SECONDS: Dict[str, int] = {
    "claude-3-opus": 300,        # Anthropic 기본 5분
    "claude-3-5-sonnet": 300,    # Anthropic 기본 5분
    "gemini-1.5-flash": 3600,    # Google Gemini 기본 1시간
    "gemini-1.5-pro": 3600,      # Google Gemini 기본 1시간
    "gpt-4o": 300                # OpenAI 기본 5분 (LRU 추정)
}

class LayeredCacheManager:
    """
    Layer 1 (Static Cache Layer) 및 TTL 수명 관리 모듈:
    - 시스템 프롬프트, 프로젝트 아키텍처 등 불변 컨텍스트 스냅샷 관리
    - 모델별 캐시 만료 타이머(TTL: 5분/1시간)를 추적하여 Cache Miss 방어
    - 만료 전 Keep-Alive Warm-up 핑을 보낼 수 있는 수명 지표 제공
    """
    def __init__(self):
        self.static_prefix_cache_id: str = "cache_snapshot_v1"
        self.cache_hits: int = 0
        self.cache_evictions: int = 0
        self.last_accessed_at: float = time.time()

    def get_model_ttl(self, model_name: str) -> int:
        """모델명에 대응하는 공식 TTL(초)을 반환 (기본값 300초=5분)"""
        lower_name = model_name.lower()
        for key, ttl in MODEL_TTL_SECONDS.items():
            if key in lower_name:
                return ttl
        return 300  # 알 수 없는 모델은 보수적으로 5분 적용

    def is_cache_valid(self, model_name: str = "gemini-1.5-flash") -> bool:
        """현재 캐시가 만료되지 않고 유효한지 검사"""
        elapsed = time.time() - self.last_accessed_at
        return elapsed < self.get_model_ttl(model_name)

    def get_ttl_remaining(self, model_name: str = "gemini-1.5-flash") -> int:
        """캐시 만료까지 남은 잔여 수명(초) 반환"""
        elapsed = time.time() - self.last_accessed_at
        remaining = self.get_model_ttl(model_name) - elapsed
        return max(0, int(remaining))

    def needs_keepalive(self, model_name: str = "gemini-1.5-flash", margin_seconds: int = 45) -> bool:
        """만료까지 margin_seconds 이하로 남아 Keep-Alive 핑이 필요한 상태인지 판별"""
        if not self.is_cache_valid(model_name):
            return False
        return self.get_ttl_remaining(model_name) <= margin_seconds

    def refresh_cache_ttl(self):
        """캐시 타임스탬프를 갱신(Touch)하여 수명을 다시 시작"""
        self.last_accessed_at = time.time()

    def analyze_token_split(
        self,
        messages: List[ChatMessage],
        model_name: str = "gemini-1.5-flash"
    ) -> Tuple[int, int, int]:
        """
        메시지 목록 및 캐시 TTL 상태를 분석하여 Layer1(캐시 토큰), Layer2(동적 토큰)를 분리.
        - 캐시 유효 시: CACHE_READ_RATIO(90% 할인 영역) 적용 및 Cache Hit 카운트
        - 캐시 만료 시: Eviction 발생 처리 후 전량 Dynamic 토큰 처리
        """
        total_chars = sum(len(m.content) for m in messages)
        estimated_total_tokens = max(100, int(total_chars / 3.5))

        if self.is_cache_valid(model_name):
            cached_tokens = int(estimated_total_tokens * CACHE_READ_RATIO)
            dynamic_tokens = estimated_total_tokens - cached_tokens
            self.cache_hits += 1
        else:
            # 캐시가 만료된 경우 첫 호출은 캐시 미스(Cache Miss) 처리
            self.cache_evictions += 1
            cached_tokens = 0
            dynamic_tokens = estimated_total_tokens

        # 이번 요청을 처리하면서 캐시 웜업/갱신 수행
        self.refresh_cache_ttl()
        return estimated_total_tokens, cached_tokens, dynamic_tokens

    def get_cache_status(self, model_name: str = "gemini-1.5-flash") -> Dict[str, Any]:
        """대시보드 및 헬스체크용 캐시 상태 요약 딕셔너리 반환"""
        return {
            "is_valid": self.is_cache_valid(model_name),
            "ttl_remaining_seconds": self.get_ttl_remaining(model_name),
            "model_ttl_seconds": self.get_model_ttl(model_name),
            "cache_hits": self.cache_hits,
            "cache_evictions": self.cache_evictions,
            "needs_keepalive": self.needs_keepalive(model_name)
        }

cache_manager = LayeredCacheManager()

