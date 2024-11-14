# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.database.mongodb import MongoDBManager
import tabula
import pandas as pd

# 使用 os.path 來構建絕對路徑
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DATA_FILE_PATH = os.path.join(BASE_DIR, 'resources', 'docs', 'N5.pdf')

def read_pdf_data(file_path):
    """讀取 PDF 文件中的表格數據"""
    if not os.path.exists(file_path):
        print(f"錯誤：找不到文件 '{file_path}'")
        print(f"當前工作目錄：{os.getcwd()}")
        print(f"檢查的完整路徑：{os.path.abspath(file_path)}")
        return []

    data = []
    try:
        dfs = tabula.read_pdf(
            file_path, 
            pages='all',
            lattice=True,
            pandas_options={'header': None}
        )
        
        for df in dfs:
            if len(df.columns) >= 2:
                for _, row in df.iterrows():
                    japanese = str(row[0]).strip()
                    explanation = str(row[1]).strip()
                    
                    if pd.notna(japanese) and pd.notna(explanation) and japanese != '' and explanation != '':
                        if not japanese.isdigit() and not explanation.isdigit():
                            data.append({
                                "japanese": japanese,
                                "rank": "N5",
                                "explanation": explanation
                            })
    except Exception as e:
        print(f"讀取 PDF 文件時發生錯誤: {e}")
        print(f"錯誤詳情: {str(e)}")
    return data

def insert_n5_data():
    """插入 N5 單字數據到 tests collection"""
    data = read_pdf_data(DATA_FILE_PATH)
    success_count = 0
    
    if not data:
        print("沒有找到有效的數據")
        return

    # 獲取 MongoDB 連接
    db_manager = MongoDBManager()
    tests_collection = db_manager.db["tests"]
    
    try:
        for word in data:
            try:
                # 插入數據到 tests collection
                result = tests_collection.insert_one(word)
                if result.inserted_id:
                    success_count += 1
                    print(f"成功插入: {word['japanese']} - {word['explanation']}")
                else:
                    print(f"插入失敗: {word['japanese']} - {word['explanation']}")
            except Exception as e:
                print(f"插入數據時發生錯誤: {word['japanese']} - {e}")
    finally:
        db_manager.close()
    
    print(f"\n總共成功插入 {success_count} 筆資料")

if __name__ == "__main__":
    insert_n5_data()