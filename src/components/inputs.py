from kivy.uix.textinput import TextInput
from kivy.metrics import dp


# ----------通用---------

class BaseTextInput(TextInput):
    """基礎輸入框"""
    def __init__(self, **kwargs):
        super().__init__(
            multiline=True,
            font_name="ChineseFont",
            font_size=dp(18),
            padding=[dp(10), dp(10), dp(10), dp(10)],
            **kwargs
        )

# ----------words_popup---------

class JapaneseTextInput(BaseTextInput):
    """日文輸入框"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.error_label = None

    def bind_error_label(self, error_label):
        """綁定錯誤提示標籤"""
        self.error_label = error_label
        self.bind(text=self.on_text_validate)

    def on_text_validate(self, instance, value):
        """驗證輸入文字"""
        if not value.strip():
            if self.error_label:
                self.error_label.text = "必須輸入單字"
            return False
        
        if not all(self._is_japanese_char(c) for c in value if c.strip()):
            if self.error_label:
                self.error_label.text = "請只輸入日文"
            return False
            
        if self.error_label:
            self.error_label.text = ""
        return True

    def insert_text(self, substring, from_undo=False):
        if not all(self._is_japanese_char(c) for c in substring if c.strip()):
            return
        return super().insert_text(substring, from_undo=from_undo)
    
    def _is_japanese_char(self, char):
        """檢查是否為日文字符"""
        return "\u3040" <= char <= "\u30ff" or "\u4e00" <= char <= "\u9fff"

class ExplanationTextInput(BaseTextInput):
    """解釋輸入框"""
    pass
