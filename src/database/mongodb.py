# -*- coding: utf-8 -*-
from pymongo import MongoClient
import logging
from .validators import WORDS_VALIDATOR

# MongoDB 配置常量
MONGODB_CONFIG = {
    "URL": "mongodb://localhost:27017/",
    "TIMEOUT": 5000,
    "DB_NAME": "japanese_db",
    "COLLECTION": "words"
}

class MongoDBManager:
    """MongoDB 管理類"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.client = None
            self.db = None
            self.collection = None
            self.initialized = True
            self._connect()
    
    def _connect(self):
        """建立 MongoDB 連接"""
        try:
            self.client = MongoClient(
                MONGODB_CONFIG["URL"], 
                serverSelectionTimeoutMS=MONGODB_CONFIG["TIMEOUT"]
            )
            self.client.server_info()  # 測試連接
            
            self._init_database()
            self._init_collection()
            self._set_validation_rules()
            
        except Exception as e:
            logging.error(f"無法連接到 MongoDB: {e}")
            self.collection = None
    
    def _init_database(self):
        """初始化數據庫"""
        db_names = self.client.list_database_names()
        if MONGODB_CONFIG["DB_NAME"] not in db_names:
            logging.info(f"創建 {MONGODB_CONFIG['DB_NAME']} 資料庫")
            self.db = self.client[MONGODB_CONFIG["DB_NAME"]]
            self.db.words.insert_one({
                "japanese": "テスト",
                "explanation": "測試用單字"
            })
        else:
            self.db = self.client[MONGODB_CONFIG["DB_NAME"]]
    
    def _init_collection(self):
        """初始化集合"""
        if MONGODB_CONFIG["COLLECTION"] not in self.db.list_collection_names():
            logging.info(f"創建 {MONGODB_CONFIG['COLLECTION']} 集合")
            self.db.create_collection(MONGODB_CONFIG["COLLECTION"])
        self.collection = self.db[MONGODB_CONFIG["COLLECTION"]]
    
    def _set_validation_rules(self):
        """設置驗證規則"""
        validator_config = {
            "collMod": MONGODB_CONFIG["COLLECTION"],
            **WORDS_VALIDATOR
        }
        self.db.command(validator_config)
    
    def get_collection(self):
        """獲取集合實例"""
        return self.collection
    
    def close(self):
        """關閉數據庫連接"""
        if self.client:
            self.client.close()

# 創建全局單例實例
db_manager = MongoDBManager()
words_collection = db_manager.get_collection()
