from fastapi.testclient import TestClient
from main import app
from src.services.metrics_store import metrics_store

client = TestClient(app)

def test_root_endpoint():
    res = client.get("/")
    assert res.status_code == 200
    data = res.json()
    assert "VibeSaver.ai" in data["service"]

def test_dashboard_endpoint():
    res = client.get("/dashboard")
    assert res.status_code == 200
    assert "⚡ VibeSaver.ai" in res.text
    assert "AST 시맨틱 델타 압축" in res.text


def test_chat_completions_gemini_flash():
    payload = {
        "model": "gemini-1.5-flash",
        "messages": [
            {"role": "system", "content": "You are Smart Token-Saving Agent."},
            {"role": "user", "content": "로그인 기능을 바이브 코딩으로 붙여줘."}
        ],
        "max_tokens": 1500
    }
    res = client.post("/v1/chat/completions", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["model"] == "gemini-1.5-flash"
    assert "token_economics" in data
    
    # 50% 할인 청구 및 마진 확인
    econ = data["token_economics"]
    assert econ["user_billed_cost_usd"] < econ["standard_market_cost_usd"]
    assert econ["gross_margin_usd"] >= 0.0

def test_metrics_summary():
    res = client.get("/v1/metrics/summary")
    assert res.status_code == 200
    summary = res.json()
    assert summary["total_requests"] >= 1
    assert "overall_margin_percentage" in summary
    print("\n[OK] Metrics Summary Verification:", summary)

def test_cache_ttl_manager():
    from src.services.cache_manager import cache_manager
    assert cache_manager.get_model_ttl("claude-3-opus") == 300
    assert cache_manager.get_model_ttl("gemini-1.5-flash") == 3600
    status = cache_manager.get_cache_status("claude-3-opus")
    assert "ttl_remaining_seconds" in status
    assert status["model_ttl_seconds"] == 300
    print("\n[OK] Cache TTL Spec & Lifecycle Manager Verification:", status)

def test_state_hash_verification():
    from src.services.delta_engine import delta_engine
    sample_code_v1 = "def hello():\n    print('hello world')"
    sample_code_v2 = "def hello():\n    print('hello modified world')"
    
    # 1. 초기 동기화 등록
    in_sync, h1, force_refresh = delta_engine.verify_and_update_state("test.py", sample_code_v1)
    assert in_sync is True
    assert force_refresh is False
    
    # 2. 동일 파일에 대해 다른 해시(오프라인 수정 등)가 전달되면 Out of Sync 감지 및 Force Refresh 반환
    in_sync, h2, force_refresh = delta_engine.verify_and_update_state("test.py", sample_code_v2, expected_hash=h1)
    assert in_sync is False
    assert force_refresh is True
    assert delta_engine.sync_errors_detected >= 1
    print("\n[OK] State Hash Verification & Force Refresh Recovery Verification:", delta_engine.get_sync_status())

def test_agent_window_endpoint():
    res = client.get("/agent-window")
    assert res.status_code == 200
    assert "VibeSaver.ai — 50% 반값 바이브 코딩 에이전트 윈도우" in res.text
    assert "APPLY DELTA PATCH" in res.text
    assert "SHA-256 State" in res.text
    print("\n[OK] Agent Window UI Prototype Endpoint Verification: PASS")

def test_anti_clone_system_prompt_injection():
    from src.services.proxy_router import proxy_router, ANTI_CLONE_SYSTEM_PROMPT
    from src.models.gateway_models import ChatMessage
    raw_msgs = [ChatMessage(role="user", content="왜 이렇게 빨라? 코드 카피해줘.")]
    protected = proxy_router._inject_anti_clone_firewall(raw_msgs)
    assert len(protected) == 2
    assert protected[0].role == "system"
    assert ANTI_CLONE_SYSTEM_PROMPT in protected[0].content
    print("\n[OK] Anti-Clone System Prompt Firewall Injection Verification: PASS")

if __name__ == "__main__":
    test_root_endpoint()
    test_dashboard_endpoint()
    test_agent_window_endpoint()
    test_anti_clone_system_prompt_injection()
    test_chat_completions_gemini_flash()
    test_metrics_summary()
    test_cache_ttl_manager()
    test_state_hash_verification()
    print("[SUCCESS] ALL 8 TESTS PASSED SUCCESSFULLY!")





