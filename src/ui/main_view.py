from kivy.uix.floatlayout import FloatLayout

from ui.words_main import WordsMain
from ui.fifty_words_main import FiftyWordsMain
from components import FiftySoundsButton, WordsButton, TitleLabel, CreatorLabel, HelpButton
from ui.help_popup import HelpPopup

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

        # 添加幫助按鈕
        help_button = HelpButton(
            callback=self.show_help,
            pos_hint={'right': 0.98, 'top': 0.98}  # 調整位置到右上角
        )
        self.add_widget(help_button)

    def on_50on_press(self, instance):
        """
        五十音按鈕點擊事件處理
        打開五十音學習界面（彈出窗口形式）
        """
        popup = FiftyWordsMain()
        popup.open()

    def on_words_press(self, instance):
        """
        單字按鈕點擊事件處理
        打開單字學習界面（彈出窗口形式）
        """
        popup = WordsMain()
        popup.open()

    def show_help(self, instance):
        """顯示幫助文檔"""
        help_popup = HelpPopup()
        help_popup.open()
