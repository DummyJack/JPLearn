# -*- coding: utf-8 -*-

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.metrics import dp
from math import ceil
from kivy.uix.label import Label
from kivy.clock import Clock

from database import words_collection
from components import ConfirmButton, CancelButton, ConfirmLabel, WordItem, LoadingIndicator

TEST_MODE = False  # 開啟測試模式

class WordManager(ScrollView):
    """單字管理器：負責單字的增刪改查和分頁顯示"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 創建垂直佈局容器
        self.layout = BoxLayout(
            orientation="vertical",
            spacing=dp(5),            # 元素間距
            size_hint_y=None,         # 高度不自動調整
            padding=[0, dp(5), 0, 0], # 上方留出5dp間距
        )
        # 綁定最小高度，確保可以正確滾動
        self.layout.bind(minimum_height=self.layout.setter("height"))
        
        # 添加載入指示器
        self.loading = LoadingIndicator(
            pos_hint={'center_x': .5, 'center_y': .5},
            size_hint=(None, None),
            size=(dp(100), dp(30))
        )
        self.layout.add_widget(self.loading)
        
        # 只添加 layout 作為唯一的子部件
        self.add_widget(self.layout)

        # 初始化分頁相關的狀態
        self.current_page = 1         # 當前頁碼
        self.items_per_page = 5       # 每頁顯示5個單字
        self.total_pages = 1          # 總頁數
        
        # 初始化搜索相關的狀態
        self.search_mode = False      # 是否處於搜索模式
        self.search_results = []      # 搜索結果列表
        self.last_search_term = ""    # 最後的搜索關鍵詞
        
        # 載入單字數據
        self.load_words_from_db()

    def search_words(self, search_term):
        """搜索單字：根據輸入的關鍵詞搜索單字"""
        try:
            self.last_search_term = search_term
            if not search_term:  # 如果搜索詞為空，返回普通顯示模式
                self.search_mode = False
                self.load_words_from_db()
                return

            # 進入搜索模式
            self.search_mode = True
            # 使用正則表達式進行模糊搜索
            self.search_results = list(
                words_collection.find(
                    {"japanese": {"$regex": search_term, "$options": "i"}}
                )
            )
            # 更新分頁信息
            self.total_pages = max(1, ceil(len(self.search_results) / self.items_per_page))
            self.current_page = 1
            self.update_view()
        except Exception as e:
            print(f"Error searching words: {str(e)}")

    def load_words_from_db(self):
        """從數據庫加載單字：根據當前頁碼和搜索狀態加載對應的單字"""
        # 清空當前佈局
        self.layout.clear_widgets()
        
        # 只在非搜索模式下顯示加載動畫
        if not self.search_mode:
            self.loading.start()
            self.layout.add_widget(self.loading)
            if TEST_MODE:
                # 測試模式：延遲1秒加載數據
                Clock.schedule_once(lambda dt: self._load_data(), 3)
                return
        
        # 非測試模式：直接加載數據
        self._load_data()

    def _load_data(self):
        """實際加載數據的方法"""
        try:
            if words_collection is None:
                raise ConnectionError("無法連接到數據庫")
            
            # 根據搜索模式決定數據來源
            if self.search_mode:
                # 從搜索結果中獲取當前頁的數據
                total_words = len(self.search_results)
                words = self.search_results[
                    (self.current_page - 1) * self.items_per_page : 
                    self.current_page * self.items_per_page
                ]
            else:
                # 從數據庫中獲取當前頁的數據
                total_words = words_collection.count_documents({})
                skip = (self.current_page - 1) * self.items_per_page
                words = list(
                    words_collection.find()
                    .sort([("_id", -1)])  # 按ID降序排序，最新添加的顯示在前面
                    .skip(skip)
                    .limit(self.items_per_page)
                )

            # 更新總頁數
            self.total_pages = max(1, ceil(total_words / self.items_per_page))

            # 添加單字到界面
            for word in words:
                self.add_word(word["japanese"], word["explanation"], word["_id"])
            
            # 如果沒有數據，顯示提示信息
            if not words:
                no_data_label = Label(
                    text="暫無數據" if not self.search_mode else "未找到匹配的單字",
                    font_name="ChineseFont",
                    font_size='24sp',
                    bold=True,
                    color=(0.8, 0.8, 0.8, 1),
                    size_hint_y=None,
                    height=dp(60),
                    halign='center',
                    valign='middle'
                )
                # 添加一個空白 Widget 來推動文字向下
                self.layout.add_widget(Widget(size_hint_y=None, height=dp(100)))
                self.layout.add_widget(no_data_label)
            
        except Exception as e:
            # 錯誤處理
            error_label = Label(
                text="加載數據時發生錯誤",
                font_name="ChineseFont",
                color=(1, 0, 0, 1)  # 紅色文字
            )
            self.layout.add_widget(error_label)
            print(f"Error loading words: {str(e)}")
            
        finally:
            # 只在非搜索模式下停止加載動畫
            if not self.search_mode:
                self.loading.stop()

    def add_word(self, japanese, explanation, word_id=None):
        """添加單字到界面"""
        word_item = WordItem(
            japanese,
            explanation,
            self.show_delete_confirmation,
            self.edit_word,
            word_id,
        )
        # 新單字添加到頂部
        if self.current_page == 1:
            self.layout.add_widget(word_item, index=0)
        else:
            self.layout.add_widget(word_item)

        # 控制每頁顯示數量
        if len(self.layout.children) > self.items_per_page:
            self.layout.remove_widget(self.layout.children[-1])

    def show_delete_confirmation(self, word_item):
        """顯示刪除確認對話框"""
        content = BoxLayout(
            orientation="vertical", 
            spacing=dp(40), 
            padding=dp(20)
        )
        content.add_widget(ConfirmLabel(text="是否刪除單字？"))

        buttons = BoxLayout(
            orientation="horizontal", 
            spacing=dp(20), 
            size_hint_y=None, 
            height=dp(50)
        )
        
        confirm_btn = ConfirmButton(
            text="確定",
            on_press=lambda x: self.delete_word(word_item, popup)
        )
        
        cancel_btn = CancelButton(
            on_press=lambda x: popup.dismiss()
        )
        
        buttons.add_widget(Widget(size_hint_x=0.5))
        buttons.add_widget(confirm_btn)
        buttons.add_widget(cancel_btn)
        buttons.add_widget(Widget(size_hint_x=0.5))
        content.add_widget(buttons)

        popup = Popup(
            content=content, 
            size_hint=(0.6, 0.3), 
            title="", 
            separator_height=0
        )

        popup.open()

    def delete_word(self, word_item, popup):
        """刪除單字並更新界面"""
        # 從數據庫中刪除
        words_collection.delete_one({"_id": word_item.word_id})
        # 從界面中移除
        self.layout.remove_widget(word_item)

        # 更新分頁信息
        total_words = words_collection.count_documents({})
        new_total_pages = max(1, ceil(total_words / self.items_per_page))

        # 如果當前頁超出範圍，調整到最後一頁
        if self.current_page > new_total_pages:
            self.current_page = new_total_pages

        self.update_view()
        popup.dismiss()

    def edit_word(self, word_item, new_japanese, new_explanation):
        """更新單字信息"""
        words_collection.update_one(
            {"_id": word_item.word_id},
            {"$set": {"japanese": new_japanese, "explanation": new_explanation}},
        )

    def update_view(self):
        """更新界面顯示：重新計算頁數並刷新顯示"""
        # 獲取總單字數
        if self.search_mode:
            total_words = len(self.search_results)
        else:
            total_words = words_collection.count_documents({})

        # 更新分頁信息
        new_total_pages = max(1, ceil(total_words / self.items_per_page))
        self.total_pages = new_total_pages
        self.current_page = min(self.current_page, self.total_pages)

        # 重新加載數據並更新分頁控件
        self.load_words_from_db()
        if hasattr(self, "parent") and hasattr(self.parent, "update_pagination"):
            self.parent.update_pagination()
