from kivy.uix.textinput import TextInput
from kivy.metrics import dp
from utils import TextValidator, JapaneseValidator
from typing import Optional

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

class ValidatedTextInput(BaseTextInput):
    """帶驗證的輸入框基類"""
    def __init__(self, validator: TextValidator = None, **kwargs):
        super().__init__(**kwargs)
        self.validator = validator
        self.error_label = None
        self.helper_text = kwargs.get('helper_text', '')
        
        # 設置初始背景色
        self.normal_background = (0.95, 0.95, 0.95, 1)  # 淺灰色
        self.error_background = (1, 0.9, 0.9, 1)      # 淺紅色
        self.success_background = (0.9, 1, 0.9, 1)    # 淺綠色
        self.background_color = self.normal_background

    def bind_error_label(self, error_label):
        """綁定錯誤提示標籤"""
        self.error_label = error_label
        self.bind(text=self.on_text_validate)
        # 添加即時驗證
        self.bind(text=self.on_text_change)

    def on_text_change(self, instance, value):
        """即時輸入驗證"""
        if not self.validator:
            return True
            
        is_valid, error_message = self.validator.validate(value)
        self._update_feedback(is_valid, error_message)
        return is_valid

    def _update_feedback(self, is_valid: bool, error_message: Optional[str]):
        """更新視覺反饋"""
        if not is_valid:
            self.background_color = self.error_background
            if self.error_label:
                self.error_label.text = error_message
        else:
            self.background_color = self.success_background if self.text.strip() else self.normal_background
            if self.error_label:
                self.error_label.text = ""

    def on_text_validate(self, instance, value):
        """驗證輸入文字"""
        if not self.validator:
            return True
            
        is_valid, error_message = self.validator.validate(value)
        if not is_valid and self.error_label:
            self.error_label.text = error_message
        elif self.error_label:
            self.error_label.text = ""
        return is_valid

    def insert_text(self, substring, from_undo=False):
        """輸入時驗證"""
        if self.validator and not self.validator.validate_char(substring):
            return
        return super().insert_text(substring, from_undo=from_undo)

# ----------words_popup---------

class JapaneseTextInput(ValidatedTextInput):
    """日文輸入框"""
    def __init__(self, **kwargs):
        super().__init__(
            validator=JapaneseValidator(),
            **kwargs
        )

class ExplanationTextInput(ValidatedTextInput):
    """解釋輸入框"""
    pass
