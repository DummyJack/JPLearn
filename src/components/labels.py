from kivy.uix.label import Label
from kivy.metrics import dp

# ----------通用---------
class BaseLabel(Label):
    """基礎標籤"""
    def __init__(self, **kwargs):
        super().__init__(
            font_name="ChineseFont",
            **kwargs
        )
        
# ----------words related---------

class ErrorLabel(BaseLabel):
    """錯誤提示標籤"""
    def __init__(self, **kwargs):
        super().__init__(
            text="",
            color=(1, 0, 0, 1),  # 紅色
            font_size=dp(14),
            size_hint_y=None,
            height=dp(30),
            **kwargs
        )

class WordLabel(BaseLabel):
    """單字標籤"""
    def __init__(self, **kwargs):
        super().__init__(
            font_size=dp(24),
            size_hint=(None, None),
            size=(dp(120), dp(70)),
            text_size=(dp(120), dp(70)),
            halign="center",
            valign="middle",
            **kwargs
        )

class ExplanationLabel(BaseLabel):
    """解釋標籤"""
    def __init__(self, **kwargs):
        super().__init__(
            font_size=dp(20),
            size_hint_y=None,
            height=dp(70),
            text_size=(dp(200), None),
            halign="left",
            valign="middle",
            **kwargs
        )
        self.bind(texture_size=self._update_height)

    def _update_height(self, instance, size):
        """更新標籤高度"""
        self.height = max(size[1], dp(70))
        if size[1] <= dp(30):
            self.valign = "middle"
            self.halign = "center"
        else:
            self.valign = "top"
            self.halign = "left"

class HeaderLabel(BaseLabel):
    """標題標籤"""
    def __init__(self, **kwargs):
        super().__init__(
            font_size=dp(28),
            **kwargs
        )

class ConfirmLabel(BaseLabel):
    """確認提示標籤"""
    def __init__(self, **kwargs):
        super().__init__(
            font_size=dp(24),
            **kwargs
        )
