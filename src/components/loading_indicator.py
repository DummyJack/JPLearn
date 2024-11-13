from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout

class LoadingIndicator(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(
            orientation="vertical",
            size_hint_y=None,
            height=dp(160),
            **kwargs
        )
        
        # 創建加載文字標籤
        self.loading_label = Label(
            text="Loading...",
            font_name="ChineseFont",
            font_size='24sp',
            bold=True,
            color=(0.8, 0.8, 0.8, 1),
            size_hint_y=None,
            height=dp(-200),
            halign='center',
            valign='middle',
            opacity=0
        )
        self.add_widget(self.loading_label)
        
    def start(self):
        Animation(opacity=1, duration=0.3).start(self.loading_label)
        
    def stop(self):
        Animation(opacity=0, duration=0.3).start(self.loading_label)
