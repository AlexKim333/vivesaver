import re
import hashlib
from typing import List, Dict, Tuple, Optional, Any
from src.models.gateway_models import ChatMessage
from src.config import DELTA_OUTPUT_RATIO

class SemanticDeltaEngine:
    """
    AST 시맨틱 델타, 패치 처리 및 상태 해시 동기화(State Hash Verification) 모듈:
    - 사용자의 대화 중 불필요한 장황어/반복문 및 비시맨틱 공백을 정제
    - LLM 응답을 파일 전체 덮어쓰기가 아닌 Diff 패치 형식으로 유도 및 압축
    - SHA-256 해시 검증으로 로컬 코드와 서버 상태 불일치(Out-of-Sync) 감지 및 자동 복구(Force Refresh)
    """
    def __init__(self):
        self.optimized_turns: int = 0
        self.file_state_hashes: Dict[str, str] = {}
        self.sync_errors_detected: int = 0
        self.force_refreshes_triggered: int = 0

    def compute_state_hash(self, content: str) -> str:
        """코드 또는 파일 컨텐츠의 SHA-256 무결성 해시값을 반환"""
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def verify_and_update_state(
        self,
        filepath: str,
        current_content: str,
        expected_hash: Optional[str] = None
    ) -> Tuple[bool, str, bool]:
        """
        파일의 실제 해시값과 기대 해시값을 비교하여 동기화 상태 검증:
        - 불일치(Out of Sync) 감지 시: sync_error 및 force_refresh 카운터 증가, Force Refresh 보정 요구 반환
        - 반환값: (is_in_sync: bool, actual_hash: str, force_refresh_needed: bool)
        """
        actual_hash = self.compute_state_hash(current_content)
        
        # 기대 해시값이 제공되었으나 실제 해시와 다를 경우 (오프라인 수정, Git 브랜치 변경 등)
        if expected_hash and expected_hash != actual_hash:
            self.sync_errors_detected += 1
            self.force_refreshes_triggered += 1
            self.file_state_hashes[filepath] = actual_hash
            return False, actual_hash, True
            
        # 기존 저장된 서버 상태가 있는데 해시가 달라진 경우도 동기화 보정
        if filepath in self.file_state_hashes and self.file_state_hashes[filepath] != actual_hash:
            self.sync_errors_detected += 1
            self.force_refreshes_triggered += 1
            self.file_state_hashes[filepath] = actual_hash
            return False, actual_hash, True

        self.file_state_hashes[filepath] = actual_hash
        return True, actual_hash, False

    def compress_input_messages(self, messages: List[ChatMessage]) -> List[ChatMessage]:
        """
        입력 메시지에서 중복 공백 및 불필요한 대용량 로그 스니펫 등을 정제하여 토큰 압축
        """
        compressed = []
        for msg in messages:
            cleaned_text = re.sub(r"\n{3,}", "\n\n", msg.content.strip())
            compressed.append(ChatMessage(role=msg.role, content=cleaned_text))
        self.optimized_turns += 1
        return compressed

    def estimate_patch_output_tokens(self, full_expected_tokens: int) -> int:
        """
        전체 파일 재출력 대비 Search & Replace 패치(Diff) 방식으로 출력했을 때의 토큰 수 산정
        """
        return max(50, int(full_expected_tokens * DELTA_OUTPUT_RATIO))

    def get_sync_status(self) -> Dict[str, Any]:
        """대시보드 및 헬스체크용 델타 동기화 상태 요약 딕셔너리 반환"""
        return {
            "tracked_files_count": len(self.file_state_hashes),
            "sync_errors_detected": self.sync_errors_detected,
            "force_refreshes_triggered": self.force_refreshes_triggered,
            "is_synchronized": self.sync_errors_detected == 0
        }

delta_engine = SemanticDeltaEngine()

