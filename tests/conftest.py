import pytest
from kivy.base import EventLoop
from kivy.core.window import Window
from kivy.core.text import LabelBase
import os


@pytest.fixture(autouse=True)
def kivy_config():
    # 使用相對路徑找到字體文件
    font_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 
                            'fonts', 
                            'NotoSansTC-VariableFont_wght.ttf')
    
    LabelBase.register(
        name="ChineseFont",
        fn_regular=font_path
    )
    
    EventLoop.ensure_window()
    yield
