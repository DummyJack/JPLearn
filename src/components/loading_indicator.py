from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout

class LoadingIndicator(BoxLayout):
    """加載指示器：顯示加載中的動畫效果"""
    def __init__(self, **kwargs):
        # 初始化基礎佈局設置
        super().__init__(
            orientation="vertical",      # 垂直佈局
            size_hint_y=None,           # 不自動調整高度
            height=dp(160),             # 固定高度為160dp
            **kwargs
        )
        
        # 創建加載文字標籤
        self.loading_label = Label(
            text="Loading...",          
            font_name="ChineseFont",    
            font_size='24sp',           
            bold=True,                  # 粗體
            color=(0.8, 0.8, 0.8, 1),   # 淺灰色文字
            size_hint_y=None,           # 不自動調整高度
            height=dp(-200),            # 負值高度用於調整位置
            halign='center',            # 水平居中
            valign='middle',            # 垂直居中
            opacity=0                   # 初始透明度為0
        )
        self.add_widget(self.loading_label)
        
    def start(self):
        """開始加載動畫：將文字淡入顯示"""
        Animation(opacity=1, duration=0.3).start(self.loading_label)
        
    def stop(self):
        """停止加載動畫：將文字淡出隱藏"""
        Animation(opacity=0, duration=0.3).start(self.loading_label)
