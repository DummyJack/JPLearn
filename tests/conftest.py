import pytest
from kivy.base import EventLoop
from kivy.core.window import Window
from kivy.context import Context
from kivy.clock import Clock
from kivy.app import App
from kivy.core.text import LabelBase
import platform


@pytest.fixture(autouse=True)
def kivy_config():
    # Register a fallback font or your actual Chinese font
    LabelBase.register(
        name="ChineseFont",
        fn_regular=r"C:\Users\Jack\Desktop\JPLearn\fonts\NotoSansTC-VariableFont_wght.ttf",
    )  # Added 'r' prefix
    # Or use a system font instead
    # LabelBase.register(name='ChineseFont', fn_regular='Arial')

    EventLoop.ensure_window()
    yield
