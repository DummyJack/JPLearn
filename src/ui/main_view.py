from kivy.uix.floatlayout import FloatLayout

from ui.words_main import WordsMain
from ui.fifty_sounds_main import FiftySoundsMain
from components import FiftySoundsButton, WordsButton, TitleLabel, CreatorLabel

class MainView(FloatLayout):
    """主視圖：應用程序的主界面，包含標題、功能按鈕和製作人信息"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # 添加標題標籤
        self.add_widget(TitleLabel())  # "日語快樂學"標題

        # 添加功能按鈕
        # 五十音學習按鈕：左側藍色按鈕
        self.btn_50on = FiftySoundsButton(self.on_50on_press)
        self.add_widget(self.btn_50on)

        # 單字學習按鈕：右側綠色按鈕
        self.btn_words = WordsButton(self.on_words_press)
        self.add_widget(self.btn_words)

        # 添加製作人信息
        self.add_widget(CreatorLabel())  # 底部的製作人信息

    def on_50on_press(self, instance):
        """
        五十音按鈕點擊事件處理
        打開五十音學習界面（彈出窗口形式）
        """
        popup = FiftySoundsMain()
        popup.open()

    def on_words_press(self, instance):
        """
        單字按鈕點擊事件處理
        打開單字學習界面（彈出窗口形式）
        """
        popup = WordsMain()
        popup.open()
