import pytest
from unittest.mock import Mock, patch
from kivy.base import EventLoop
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp
from functions.fifty_sounds import FiftySoundsGrid, FiftySoundsPopup


@pytest.fixture(scope="module", autouse=True)
def setup_kivy():
    """設置 Kivy 測試環境"""
    EventLoop.ensure_window()
    Window.size = (800, 600)
    yield
    Window.size = (800, 600)


@pytest.fixture
def fifty_sounds_grid():
    """提供 FiftySoundsGrid 實例"""
    return FiftySoundsGrid()


@pytest.fixture
def mock_audio():
    """提供模擬的音頻對象"""
    audio = Mock()
    audio.length = 1.0
    audio.play = Mock()
    audio.stop = Mock()
    return audio


def test_grid_layout(fifty_sounds_grid):
    """測試網格布局的基本屬性和按鈕配置"""
    # 獲取所有按鈕
    buttons = [
        btn for child in fifty_sounds_grid.children 
        if isinstance(child, BoxLayout)
        for btn in child.children 
        if isinstance(btn, Button)
    ]
    
    assert buttons, "應該至少有一個按鈕"
    
    first_button = buttons[0]
    assert tuple(first_button.size_hint) == (None, None)
    assert dp(60) <= first_button.size[1] <= dp(220)


@patch('kivy.core.audio.SoundLoader.load')
def test_play_sound(mock_load, fifty_sounds_grid, mock_audio):
    """測試音效播放功能"""
    mock_load.return_value = mock_audio
    
    test_button = Button(
        text="[size=30]あ[/size]\n[size=24]a[/size]",
        markup=True
    )
    
    fifty_sounds_grid.play_sound(test_button)
    
    mock_load.assert_called_once()
    mock_audio.play.assert_called_once()
    assert fifty_sounds_grid.current_button == test_button
    assert fifty_sounds_grid.current_audio == mock_audio


def test_reset_other_buttons(fifty_sounds_grid):
    """測試重置其他按鈕顏色的功能"""
    test_layout = BoxLayout()
    test_buttons = [
        Button(
            text=f"[size=30]あ{i}[/size]\n[size=24]a{i}[/size]",
            markup=True,
            background_color=(1, 0, 0, 1)
        ) for i in range(3)
    ]
    
    for btn in test_buttons:
        test_layout.add_widget(btn)
    
    fifty_sounds_grid.add_widget(test_layout)
    
    fifty_sounds_grid._reset_other_buttons(test_buttons[0])
    
    for btn in test_buttons[1:]:
        assert tuple(btn.background_color) == (0.5, 0.7, 1, 1)
    
    fifty_sounds_grid.remove_widget(test_layout)
