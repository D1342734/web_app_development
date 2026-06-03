import sqlite3
import os
from flask import g, current_app

def get_db():
    """取得資料庫連線，並將連線物件綁定在 Flask g 物件中"""
    if 'db' not in g:
        # 確保 instance 目錄存在
        os.makedirs(current_app.instance_path, exist_ok=True)
        db_path = os.path.join(current_app.instance_path, 'database.db')
        
        g.db = sqlite3.connect(db_path)
        # 設定回傳型態為 Row 物件，可透過欄位名稱存取欄位值
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    """關閉目前請求的資料庫連線"""
    db = g.pop('db', None)
    if db is not None:
        db.close()
