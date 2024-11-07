from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.metrics import dp

from database import words_collection
from components import JapaneseTextInput, ExplanationTextInput, ErrorLabel, CancelButton, ConfirmButton

class WordPopup(Popup):
    """單字彈窗（新增和編輯）"""
    def __init__(self, callback, update_view_callback, mode="add", japanese="", explanation="", word_id=None, **kwargs):
        # 確保 japanese 和 explanation 是字符串
        japanese = str(japanese) if japanese else ""
        explanation = str(explanation) if explanation else ""
        
        super().__init__(**kwargs)
        self.title = ""
        self.separator_height = 0
        self.size_hint = (0.9, 0.6)
        
        self.mode = mode  # "add" 或 "edit"
        self.callback = callback
        self.update_view_callback = update_view_callback
        self.word_id = word_id

        layout = BoxLayout(orientation="vertical", spacing=dp(20), padding=dp(20))

        # 輸入框佈局
        input_layout = BoxLayout(
            orientation="horizontal", 
            spacing=dp(10), 
            size_hint_y=None, 
            height=dp(150)
        )

        # 錯誤提示標籤
        self.error_label = ErrorLabel()

        # 日文輸入框
        self.japanese_input = JapaneseTextInput(
            text=japanese,
            hint_text="輸入單字",
            size_hint_x=0.3,
        )
        self.japanese_input.bind_error_label(self.error_label)
        input_layout.add_widget(self.japanese_input)

        # 解釋輸入框
        self.explanation_input = ExplanationTextInput(
            text=explanation,
            hint_text="請輸入解釋",
            size_hint_x=0.7,
        )
        input_layout.add_widget(self.explanation_input)

        layout.add_widget(input_layout)
        layout.add_widget(self.error_label)

        # 按鈕佈局
        button_layout = BoxLayout(
            orientation="horizontal", 
            spacing=dp(20), 
            size_hint_y=None, 
            height=dp(40)
        )

        # 根據模式設置按鈕文字
        action_button = ConfirmButton(
            text="新增" if mode == "add" else "修改",
            on_press=self.submit_form,
        )

        cancel_button = CancelButton(
            on_press=self.dismiss,
        )

        button_layout.add_widget(Widget())
        button_layout.add_widget(action_button)
        button_layout.add_widget(cancel_button)
        button_layout.add_widget(Widget())

        layout.add_widget(button_layout)
        self.content = layout

    def submit_form(self, instance):
        """提交表單（新增或編輯）"""
        japanese = self.japanese_input.text.strip()
        explanation = self.explanation_input.text.strip()

        if not self.japanese_input.on_text_validate(None, japanese):
            return

        explanation = explanation if explanation else ""
        
        if self.mode == "add":
            # 新增模式
            if words_collection is None:
                self.error_label.text = "資料庫連接失敗"
                return

            try:
                result = words_collection.insert_one(
                    {"japanese": japanese, "explanation": explanation}
                )
                self.callback(japanese, explanation, result.inserted_id)
                self.dismiss()
                self.update_view_callback()
            except Exception as e:
                self.error_label.text = f"新增失敗: {str(e)}"
        else:
            # 編輯模式
            self.callback(japanese, explanation)
            self.dismiss()
