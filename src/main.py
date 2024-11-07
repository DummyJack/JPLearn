# -*- coding: utf-8 -*-

from kivy.app import App
from kivy.core.window import Window
from kivy.core.text import LabelBase
from ui import MainView


class JapaneseLearnApp(App):
    def build(self):
        # 註冊中文字體
        LabelBase.register(
            name="ChineseFont",
            fn_regular="resources/fonts/NotoSansTC-VariableFont_wght.ttf",
        )
        Window.size = (1080, 720)  # 設置固定視窗大小
        Window.clearcolor = (0.94, 0.97, 1, 1)  # 設置窗口背景顏色為淺藍色
        return MainView()


if __name__ == "__main__":
    JapaneseLearnApp().run()
