import pytest
from coverage import Coverage
from kivy.base import EventLoop
from kivy.core.window import Window
from kivy.core.text import LabelBase
import os

@pytest.fixture(autouse=True)
def coverage_cleanup():
    """確保每次測試運行前都有乾淨的 coverage 數據"""
    # 清理舊的覆蓋率數據
    if os.path.exists(".coverage"):
        try:
            os.chmod(".coverage", 0o666)
            os.remove(".coverage")
        except Exception as e:
            print(f"清理 coverage 文件時出錯: {e}")
    
    # 啟動新的覆蓋率收集
    cov = Coverage()
    cov.start()
    
    yield
    
    # 停止覆蓋率收集並保存
    try:
        cov.stop()
        cov.save()
    except Exception as e:
        print(f"保存 coverage 數據時出錯: {e}")

@pytest.fixture(autouse=True)
def kivy_config():
    """配置 Kivy 環境"""
    # 設置字體
    font_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), 
        'fonts', 
        'NotoSansTC-VariableFont_wght.ttf'
    )
    
    LabelBase.register(
        name="ChineseFont",
        fn_regular=font_path
    )
    
    # 初始化 Kivy 窗口
    EventLoop.ensure_window()
    
    yield

@pytest.fixture(autouse=True)
def setup_kivy():
    """設置 Kivy 測試環境"""
    # 設置初始窗口大小
    Window.size = (800, 600)
    
    yield
    
    # 重置窗口大小
    Window.size = (800, 600)
