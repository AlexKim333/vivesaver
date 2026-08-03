import httpx
from typing import List, Tuple, Optional
from src.models.gateway_models import ChatMessage
from src.config import config

class GeminiFlashClient:
    """
    Google Gemini Flash API 연동 모듈 (httpx REST 호출)
    """
    def __init__(self):
        self.base_url = "https://generativelanguage.googleapis.com/v1beta/models"

    async def generate_content(
        self,
        messages: List[ChatMessage],
        model_name: str = "gemini-1.5-flash",
        api_key: Optional[str] = None
    ) -> Tuple[str, Optional[dict]]:
        """
        Gemini API 호출 및 응답 텍스트 + 사용량 메타데이터 반환
        """
        key = api_key or config.GEMINI_API_KEY
        if not key:
            return None, None
            
        # 메시지를 Gemini API 형식(contents -> parts)으로 변환
        contents = []
        for msg in messages:
            role = "user" if msg.role in ("user", "system") else "model"
            contents.append({
                "role": role,
                "parts": [{"text": msg.content}]
            })
            
        url = f"{self.base_url}/{model_name}:generateContent?key={key}"
        payload = {
            "contents": contents,
            "generationConfig": {
                "temperature": 0.2,
                "maxOutputTokens": 2048
            }
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post(url, json=payload)
            if resp.status_code != 200:
                raise RuntimeError(f"Gemini API Error ({resp.status_code}): {resp.text}")
            data = resp.json()
            
            # 텍스트 추출
            reply_text = ""
            try:
                reply_text = data["candidates"][0]["content"]["parts"][0]["text"]
            except (KeyError, IndexError):
                reply_text = "[Gemini Empty Response]"
                
            # 메타데이터 (usageMetadata) 추출
            usage_meta = data.get("usageMetadata", None)
            return reply_text, usage_meta

gemini_client = GeminiFlashClient()
