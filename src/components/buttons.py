from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle

# ----------通用---------

class ButtonWithIcon(ButtonBehavior, BoxLayout):
    """帶圖標的按鈕基類"""
    def __init__(self, icon, size, with_background=True, icon_size_ratio=0.6, padding_left=0, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = size
        self.orientation = "vertical"

        if with_background:
            with self.canvas.before:
                Color(0.8, 0.8, 0.8, 1)
                self.bg = RoundedRectangle(
                    pos=self.pos,
                    size=self.size,
                    radius=[5]
                )
            self.bind(pos=self.update_bg, size=self.update_bg)

        icon_layout = AnchorLayout(
            anchor_x="center",
            anchor_y="center",
            size_hint=(1, 1),
            padding=[padding_left, 0, 0, 0]
        )

        if icon == "+":
            add_label = Label(
                text="+",
                font_size=dp(30),
                color=(0, 0, 0, 1),
                bold=True
            )
            icon_layout.add_widget(add_label)
        else:
            icon_size = (size[0] * icon_size_ratio, size[1] * icon_size_ratio)
            icon_image = Image(
                source=icon,
                size_hint=(None, None),
                size=icon_size
            )
            icon_layout.add_widget(icon_image)

        self.add_widget(icon_layout)

    def update_bg(self, *args):
        if hasattr(self, 'bg'):
            self.bg.pos = self.pos
            self.bg.size = self.size

class ButtonWithBackground(Button):
    """帶背景的基礎按鈕"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)
        with self.canvas.before:
            Color(0.7, 0.7, 0.7, 1)
            self.bg = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[5]
            )
        self.color = (0.2, 0.2, 0.2, 1)
        self.bind(pos=self.update_bg, size=self.update_bg)

    def update_bg(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size

# ----------words_popup---------

class AddButton(ButtonWithIcon):
    """新增按鈕"""
    def __init__(self, callback, **kwargs):
        super().__init__(
            icon="+", 
            size=(dp(40), dp(40)), 
            with_background=True,
            padding=[0, 0, 0, 0],
            **kwargs
        )
        self.bind(on_press=callback)

class EditButton(ButtonWithIcon):
    """編輯按鈕"""
    def __init__(self, callback, **kwargs):
        super().__init__(
            icon="resources/icons/edit_icon.png", 
            size=(dp(40), dp(40)),
            with_background=False,
            icon_size_ratio=0.8,
            **kwargs
        )
        self.bind(on_press=callback)

class DeleteButton(ButtonWithIcon):
    """刪除按鈕"""
    def __init__(self, callback, **kwargs):
        super().__init__(
            icon="resources/icons/delete_icon.png", 
            size=(dp(40), dp(40)),
            with_background=False,
            icon_size_ratio=0.8,
            **kwargs
        )
        self.bind(on_press=callback)

class ConfirmButton(ButtonWithBackground):
    """確認按鈕"""
    def __init__(self, **kwargs):
        super().__init__(
            font_name="ChineseFont",
            font_size=dp(18),
            size_hint=(None, None),
            size=(dp(100), dp(50)),
            **kwargs
        )

class CancelButton(ButtonWithBackground):
    """取消按鈕"""
    def __init__(self, **kwargs):
        super().__init__(
            text="取消",
            font_name="ChineseFont",
            font_size=dp(18),
            size_hint=(None, None),
            size=(dp(100), dp(50)),
            **kwargs
        )

# ----------fifty_sounds---------

class SoundButton(Button):
    """五十音按鈕"""
    def __init__(self, japanese, romaji, size=dp(70), **kwargs):
        super().__init__(
            text=f"[size=30]{japanese}[/size]\n[size=24]{romaji}[/size]",
            markup=True,
            font_name="ChineseFont",
            background_color=(0.5, 0.7, 1, 1),
            size_hint=(None, None),
            size=(size, size),
            halign="center",
            valign="middle",
            text_size=(size, size),
            **kwargs
        )

class SongButton(Button):
    """五十音歌曲按鈕"""
    def __init__(self, size=dp(70), **kwargs):
        super().__init__(
            text="一首歌記住五十音",
            font_name="ChineseFont",
            background_color=(1, 0.7, 0.7, 1),  # COLORS["SONG_INITIAL"]
            size_hint=(None, None),
            size=(size * 3, size),
            halign="center",
            valign="middle",
            **kwargs
        )
