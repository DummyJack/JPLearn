# -*- coding: utf-8 -*-

from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.metrics import dp

from database import words_collection
from components import JapaneseTextInput, ExplanationTextInput, ErrorLabel, CancelButton, ConfirmButton
from ui.confirm_popup import ConfirmPopup

class WordPopup(Popup):
    """單字彈窗：用於新增和編輯單字的彈出窗口"""
    def __init__(self, callback, update_view_callback, mode="add", japanese="", explanation="", word_id=None, **kwargs):
        """
        初始化單字彈窗
        Args:
            callback: 提交表單後的回調函數
            update_view_callback: 更新主視圖的回調函數
            mode: 模式，"add"為新增，"edit"為編輯
            japanese: 日語單字（編輯模式時使用）
            explanation: 單字解釋（編輯模式時使用）
            word_id: 單字ID（編輯模式時使用）
        """
        # 確保輸入值為字符串類型
        japanese = str(japanese) if japanese else ""
        explanation = str(explanation) if explanation else ""
        
        super().__init__(**kwargs)
        # 設置彈窗基本屬性
        self.title = ""               # 無標題
        self.separator_height = 0     # 無分隔線
        self.size_hint = (0.9, 0.6)  # 佔屏幕90%寬度，60%高度
        
        self.mode = mode             # 設置模式: "add" 或 "edit"
        self.callback = callback      # 保存回調函數
        self.update_view_callback = update_view_callback  # 保存視圖更新回調
        self.word_id = word_id       # 保存單字ID

        # 創建主佈局容器
        layout = BoxLayout(
            orientation="vertical",    # 垂直佈局
            spacing=dp(20),           # 元素間距20dp
            padding=dp(20)            # 內邊距20dp
        )

        # 創建輸入區域佈局
        input_layout = BoxLayout(
            orientation="horizontal",  # 水平佈局
            spacing=dp(10),           # 元素間距10dp
            size_hint_y=None,         # 高度不自動調整
            height=dp(150)            # 固定高度150dp
        )

        # 創建錯誤提示標籤
        self.error_label = ErrorLabel()

        # 創建日文輸入框
        self.japanese_input = JapaneseTextInput(
            text=japanese,            # 設置初始文本
            hint_text="輸入單字",      # 設置提示文字
            size_hint_x=0.3,          # 佔總寬度30%
        )
        self.japanese_input.bind_error_label(self.error_label)  # 綁定錯誤提示標籤
        input_layout.add_widget(self.japanese_input)

        # 創建解釋輸入框
        self.explanation_input = ExplanationTextInput(
            text=explanation,         # 設置初始文本
            hint_text="請輸入解釋",    # 設置提示文字
            size_hint_x=0.7,          # 佔總寬度70%
        )
        input_layout.add_widget(self.explanation_input)

        # 將輸入區域和錯誤提示添加到主佈局
        layout.add_widget(input_layout)
        layout.add_widget(self.error_label)

        # 創建按鈕區域佈局
        button_layout = BoxLayout(
            orientation="horizontal",  # 水平佈局
            spacing=dp(20),           # 按鈕間距20dp
            size_hint_y=None,         # 高度不自動調整
            height=dp(40)             # 固定高度40dp
        )

        # 創建確認按鈕（根據模式顯示不同文字）
        action_button = ConfirmButton(
            text="新增" if mode == "add" else "修改",
            on_press=self.submit_form,
        )

        # 創建取消按鈕
        cancel_button = CancelButton(
            on_press=self.dismiss,
        )

        # 添加按鈕到佈局（使用Widget添加空白區域實現居中效果）
        button_layout.add_widget(Widget())  # 左側空白
        button_layout.add_widget(action_button)
        button_layout.add_widget(cancel_button)
        button_layout.add_widget(Widget())  # 右側空白

        # 將按鈕區域添加到主佈局
        layout.add_widget(button_layout)
        self.content = layout

    def submit_form(self, instance):
        """
        提交表單：驗證輸入並顯示確認對話框
        Args:
            instance: 按鈕實例
        """
        # 獲取並清理輸入值
        japanese = self.japanese_input.text.strip()
        explanation = self.explanation_input.text.strip()

        # 驗證日文輸入
        if not self.japanese_input.on_text_validate(None, japanese):
            return

        # 準備確認對話框的內容
        content_text = (
            f"單字：{japanese}\n"
            f"解釋：{explanation or ''}"
        )

        # 定義確認後的回調函數
        def on_confirm():
            self._perform_submit(japanese, explanation)

        # 顯示確認對話框
        confirm_popup = ConfirmPopup(
            content_text=content_text,
            on_confirm=on_confirm
        )
        confirm_popup.open()

    def _perform_submit(self, japanese: str, explanation: str):
        """
        執行實際的提交操作：根據模式執行新增或修改
        Args:
            japanese: 日文單字
            explanation: 單字解釋
        """
        try:
            if self.mode == "add":
                # 新增模式：檢查數據庫連接並插入新記錄
                if words_collection is None:
                    self.error_label.text = "資料庫連接失敗"
                    return

                result = words_collection.insert_one({
                    "japanese": japanese,
                    "explanation": explanation
                })
                self.callback(japanese, explanation, result.inserted_id)
            else:
                # 編輯模式：直接調用回調函數
                self.callback(japanese, explanation)

            # 關閉彈窗並更新視圖
            self.dismiss()
            self.update_view_callback()
            
        except Exception as e:
            # 顯示錯誤信息
            self.error_label.text = f"{'新增' if self.mode == 'add' else '修改'}失敗: {str(e)}"
