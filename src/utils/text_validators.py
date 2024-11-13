from typing import Tuple, Optional
from abc import ABC, abstractmethod

class TextValidator(ABC):
    """文字驗證器基類：定義文字驗證的基本接口"""
    @abstractmethod
    def validate(self, text: str) -> Tuple[bool, Optional[str]]:
        """
        驗證文字內容
        Args:
            text: 要驗證的文字
        Returns:
            Tuple[bool, Optional[str]]: (驗證是否通過, 錯誤信息)
        """
        pass

    @abstractmethod
    def validate_char(self, char: str) -> bool:
        """
        驗證輸入字符
        Args:
            char: 要驗證的字符
        Returns:
            bool: 字符是否合法
        """
        pass

class JapaneseValidator(TextValidator):
    """日文文字驗證器：確保輸入內容為日文字符"""
    def validate(self, text: str) -> Tuple[bool, Optional[str]]:
        """
        驗證日文文字
        Args:
            text: 要驗證的文字
        Returns:
            Tuple[bool, Optional[str]]: (驗證是否通過, 錯誤信息)
        """
        # 檢查是否為空
        if not text.strip():
            return False, "不可空白"
        
        # 檢查是否全部為日文字符
        if not all(self._is_japanese_char(c) for c in text if c.strip()):
            return False, "請只輸入日文（平假名、片假名或漢字）"
            
        return True, None

    def validate_char(self, char: str) -> bool:
        """
        驗證輸入的字符是否為日文
        Args:
            char: 要驗證的字符
        Returns:
            bool: 是否為合法的日文字符
        """
        return all(self._is_japanese_char(c) for c in char if c.strip())
    
    def _is_japanese_char(self, char: str) -> bool:
        """
        檢查是否為日文字符
        Args:
            char: 要檢查的字符
        Returns:
            bool: 是否為日文字符
            
        Unicode範圍:
        - \u3040-\u30ff: 平假名和片假名
        - \u4e00-\u9fff: 漢字
        """
        return "\u3040" <= char <= "\u30ff" or "\u4e00" <= char <= "\u9fff"