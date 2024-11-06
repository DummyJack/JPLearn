from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.metrics import dp

from ui import WordsMain, FiftySoundsMain

class MainView(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # 添加標題
        title = Label(
            text="日語快樂學",
            font_size=dp(60),
            size_hint_y=None,
            height=dp(100),
            color=(0, 0, 0, 1),  # 黑色文字
            pos_hint={"top": 0.95, "center_x": 0.5},  # 設置標題位置
            font_name="ChineseFont",  # 使用中文字體
        )
        self.add_widget(title)

        # 創建按鈕
        button_width = dp(250)  # 設置按鈕寬度
        button_height = dp(80)  # 設置按鈕高度

        # 創建"五十音"按鈕
        self.btn_50on = Button(
            text="五十音",
            font_size=dp(36),
            size_hint=(None, None),
            size=(button_width, button_height),
            background_color=(0, 0, 1, 1),  # 藍色背景
            pos_hint={"center_x": 0.3, "center_y": 0.5},  # 設置按鈕位置
            font_name="ChineseFont",
        )
        self.btn_50on.bind(on_press=self.on_50on_press)  # 綁定按鈕點擊事件
        self.add_widget(self.btn_50on)

        # 創建"單字"按鈕
        self.btn_words = Button(
            text="單字",
            font_size=dp(36),
            size_hint=(None, None),
            size=(button_width, button_height),
            background_color=(0, 1, 0, 1),  # 綠色背景
            pos_hint={"center_x": 0.7, "center_y": 0.5},  # 設置按鈕位置
            font_name="ChineseFont",
        )
        self.btn_words.bind(on_press=self.on_words_press)  # 綁定按鈕點擊事件
        self.add_widget(self.btn_words)

        # 添加製作人文字
        creator_label = Label(
            text="製作人：Cursor、書賢",
            font_size=dp(24),
            size_hint_y=None,
            height=dp(30),
            pos_hint={"center_x": 0.5, "y": 0.02},  # 設置標籤位置
            color=(0, 0, 0, 1),  # 黑色文字
            font_name="ChineseFont",
        )
        self.add_widget(creator_label)

    def on_50on_press(self, instance):
        # 當"五十音"按鈕被點擊時，打開五十音彈出窗口
        popup = FiftySoundsMain()
        popup.open()

    def on_words_press(self, instance):
        popup = WordsMain()
        popup.open()
