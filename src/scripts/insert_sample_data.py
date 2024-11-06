import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.database.crud import WordCRUD

# 準備8筆日文單字資料
sample_words = [
    {
        "japanese": "こんにちは",
        "explanation": "你好（白天使用）"
    },
    {
        "japanese": "ありがとう",
        "explanation": "謝謝"
    },
    {
        "japanese": "さようなら",
        "explanation": "再見"
    },
    {
        "japanese": "おはよう",
        "explanation": "早安"
    },
    {
        "japanese": "すみません",
        "explanation": "對不起；不好意思"
    },
    {
        "japanese": "いただきます",
        "explanation": "開動前的感謝用語"
    },
    {
        "japanese": "おやすみなさい",
        "explanation": "晚安"
    },
    {
        "japanese": "はじめまして",
        "explanation": "初次見面"
    }
]

def insert_sample_data():
    success_count = 0
    for word in sample_words:
        result = WordCRUD.create_word(
            japanese=word["japanese"],
            explanation=word["explanation"]
        )
        if result:
            success_count += 1
            print(f"成功插入: {word['japanese']}")
        else:
            print(f"插入失敗: {word['japanese']}")
    
    print(f"\n總共成功插入 {success_count} 筆資料")

if __name__ == "__main__":
    insert_sample_data()
