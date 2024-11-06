# -*- coding: utf-8 -*-
from typing import Optional, List, Dict, Any
from bson import ObjectId
import logging
from .mongodb import words_collection

class WordCRUD:
    """單字 CRUD 操作類"""
    
    @staticmethod
    def create_word(japanese: str, explanation: str) -> Optional[ObjectId]:
        """
        創建新單字
        
        Args:
            japanese: 日文單字
            explanation: 解釋
            
        Returns:
            ObjectId: 新創建單字的 ID
        """
        try:
            result = words_collection.insert_one({
                "japanese": japanese,
                "explanation": explanation
            })
            return result.inserted_id
        except Exception as e:
            logging.error(f"創建單字失敗: {e}")
            return None

    @staticmethod
    def get_words(skip: int = 0, limit: int = 5, sort_by: str = "_id", 
                  sort_order: int = -1) -> List[Dict[str, Any]]:
        """
        獲取單字列表
        
        Args:
            skip: 跳過的數量
            limit: 返回的數量
            sort_by: 排序字段
            sort_order: 排序方向 (1: 升序, -1: 降序)
            
        Returns:
            List[Dict]: 單字列表
        """
        try:
            return list(words_collection.find()
                       .sort([(sort_by, sort_order)])
                       .skip(skip)
                       .limit(limit))
        except Exception as e:
            logging.error(f"獲取單字列表失敗: {e}")
            return []

    @staticmethod
    def search_words(search_term: str) -> List[Dict[str, Any]]:
        """
        搜索單字
        
        Args:
            search_term: 搜索關鍵詞
            
        Returns:
            List[Dict]: 搜索結果
        """
        try:
            return list(words_collection.find(
                {"japanese": {"$regex": search_term, "$options": "i"}}
            ))
        except Exception as e:
            logging.error(f"搜索單字失敗: {e}")
            return []

    @staticmethod
    def update_word(word_id: ObjectId, japanese: str, 
                   explanation: str) -> bool:
        """
        更新單字
        
        Args:
            word_id: 單字 ID
            japanese: 新的日文單字
            explanation: 新的解釋
            
        Returns:
            bool: 是否更新成功
        """
        try:
            result = words_collection.update_one(
                {"_id": word_id},
                {"$set": {
                    "japanese": japanese,
                    "explanation": explanation
                }}
            )
            return result.modified_count > 0
        except Exception as e:
            logging.error(f"更新單字失敗: {e}")
            return False

    @staticmethod
    def delete_word(word_id: ObjectId) -> bool:
        """
        刪除單字
        
        Args:
            word_id: 單字 ID
            
        Returns:
            bool: 是否刪除成功
        """
        try:
            result = words_collection.delete_one({"_id": word_id})
            return result.deleted_count > 0
        except Exception as e:
            logging.error(f"刪除單字失敗: {e}")
            return False

    @staticmethod
    def get_total_count() -> int:
        """
        獲取單字總數
        
        Returns:
            int: 單字總數
        """
        try:
            return words_collection.count_documents({})
        except Exception as e:
            logging.error(f"獲取單字總數失敗: {e}")
            return 0
