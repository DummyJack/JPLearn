from typing import Tuple, Optional
from abc import ABC, abstractmethod

class TextValidator(ABC):
    """文字驗證器基類"""
    @abstractmethod
    def validate(self, text: str) -> Tuple[bool, Optional[str]]:
        """驗證文字內容"""
        pass

    @abstractmethod
    def validate_char(self, char: str) -> bool:
        """驗證輸入字符"""
        pass

class JapaneseValidator(TextValidator):
    """日文文字驗證器"""
    def validate(self, text: str) -> Tuple[bool, Optional[str]]:
        if not text.strip():
            return False, "必須輸入單字"
        
        if not all(self._is_japanese_char(c) for c in text if c.strip()):
            return False, "請只輸入日文"
            
        return True, None

    def validate_char(self, char: str) -> bool:
        return all(self._is_japanese_char(c) for c in char if c.strip())
    
    def _is_japanese_char(self, char: str) -> bool:
        """檢查是否為日文字符"""
        return "\u3040" <= char <= "\u30ff" or "\u4e00" <= char <= "\u9fff"