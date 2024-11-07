from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.widget import Widget
from kivy.metrics import dp

from database import words_collection
from components import JapaneseTextInput, ExplanationTextInput, ErrorLabel, CancelButton, ConfirmButton

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
        
        self.mode = mode  # "add" 或 "edit"
        self.callback = callback
        self.update_view_callback = update_view_callback
        self.word_id = word_id

        # 創建主佈局
        layout = BoxLayout(
            orientation="vertical", 
            spacing=dp(20),           # 元素間距
            padding=dp(20)            # 內邊距
        )

        # 創建輸入區域佈局
        input_layout = BoxLayout(
            orientation="horizontal", 
            spacing=dp(10), 
            size_hint_y=None, 
            height=dp(150)            # 固定高度
        )

        # 錯誤提示標籤
        self.error_label = ErrorLabel()

        # 日文輸入框
        self.japanese_input = JapaneseTextInput(
            text=japanese,
            hint_text="輸入單字",
            size_hint_x=0.3,          # 佔30%寬度
        )
        self.japanese_input.bind_error_label(self.error_label)
        input_layout.add_widget(self.japanese_input)

        # 解釋輸入框
        self.explanation_input = ExplanationTextInput(
            text=explanation,
            hint_text="請輸入解釋",
            size_hint_x=0.7,          # 佔70%寬度
        )
        input_layout.add_widget(self.explanation_input)

        # 添加輸入區域和錯誤提示
        layout.add_widget(input_layout)
        layout.add_widget(self.error_label)

        # 創建按鈕區域
        button_layout = BoxLayout(
            orientation="horizontal", 
            spacing=dp(20), 
            size_hint_y=None, 
            height=dp(40)             # 固定高度
        )

        # 根據模式設置確認按鈕文字
        action_button = ConfirmButton(
            text="新增" if mode == "add" else "修改",
            on_press=self.submit_form,
        )

        # 取消按鈕
        cancel_button = CancelButton(
            on_press=self.dismiss,
        )

        # 添加按鈕到佈局（使用Widget添加空白區域實現居中效果）
        button_layout.add_widget(Widget())
        button_layout.add_widget(action_button)
        button_layout.add_widget(cancel_button)
        button_layout.add_widget(Widget())

        layout.add_widget(button_layout)
        self.content = layout

    def submit_form(self, instance):
        """提交表單：處理新增或編輯操作"""
        # 獲取並清理輸入內容
        japanese = self.japanese_input.text.strip()
        explanation = self.explanation_input.text.strip()

        # 驗證日語輸入
        if not self.japanese_input.on_text_validate(None, japanese):
            return

        # 確保explanation不為None
        explanation = explanation if explanation else ""
        
        if self.mode == "add":
            # 新增模式：向數據庫添加新記錄
            if words_collection is None:
                self.error_label.text = "資料庫連接失敗"
                return

            try:
                # 插入數據並執行回調
                result = words_collection.insert_one(
                    {"japanese": japanese, "explanation": explanation}
                )
                self.callback(japanese, explanation, result.inserted_id)
                self.dismiss()
                self.update_view_callback()
            except Exception as e:
                self.error_label.text = f"新增失敗: {str(e)}"
        else:
            # 編輯模式：更新現有記錄
            self.callback(japanese, explanation)
            self.dismiss()
