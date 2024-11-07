from kivy.uix.floatlayout import FloatLayout

from ui.words_main import WordsMain
from ui.fifty_sounds_main import FiftySoundsMain
from components import FiftySoundsButton, WordsButton, TitleLabel, CreatorLabel

class MainView(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # 添加標題
        self.add_widget(TitleLabel())

        # 添加按鈕
        self.btn_50on = FiftySoundsButton(self.on_50on_press)
        self.add_widget(self.btn_50on)

        self.btn_words = WordsButton(self.on_words_press)
        self.add_widget(self.btn_words)

        # 添加製作人文字
        self.add_widget(CreatorLabel())

    def on_50on_press(self, instance):
        # 當"五十音"按鈕被點擊時，打開五十音彈出窗口
        popup = FiftySoundsMain()
        popup.open()

    def on_words_press(self, instance):
        popup = WordsMain()
        popup.open()
