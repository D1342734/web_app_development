import sqlite3
import sys
from app.db import get_db

class Task:
    def __init__(self, id, title, description, status, created_at):
        """
        初始化任務物件。
        
        參數:
            id (int): 任務 ID
            title (str): 任務標題
            description (str): 任務描述
            status (str): 任務狀態 ('pending' 或 'completed')
            created_at (str): 建立時間
        """
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.created_at = created_at

    @staticmethod
    def from_row(row):
        """
        將 sqlite3.Row 物件轉換成 Task 實例。
        
        參數:
            row (sqlite3.Row): 資料庫回傳的一列資料
            
        回傳:
            Task: 轉換後的 Task 物件，若 row 為 None 則回傳 None
        """
        if row is None:
            return None
        return Task(
            id=row['id'],
            title=row['title'],
            description=row['description'],
            status=row['status'],
            created_at=row['created_at']
        )

    @classmethod
    def create(cls, title, description=None):
        """
        新增一筆任務到資料庫中。
        
        參數:
            title (str): 任務標題
            description (str, optional): 任務描述
            
        回傳:
            int: 新增成功回傳任務 ID，發生異常時回傳 None
        """
        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                "INSERT INTO tasks (title, description, status) VALUES (?, ?, 'pending')",
                (title.strip(), (description or '').strip())
            )
            db.commit()
            return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"資料庫新增任務失敗: {e}", file=sys.stderr)
            return None

    @classmethod
    def get_all(cls, status=None, keyword=None):
        """
        獲取所有任務清單，支援依狀態篩選與關鍵字搜尋，按建立時間由新到舊排序。
        
        參數:
            status (str, optional): 篩選完成狀態 ('pending', 'completed')
            keyword (str, optional): 搜尋標題或描述的關鍵字
            
        回傳:
            list[Task]: 任務物件列表，發生異常時回傳空列表 []
        """
        try:
            db = get_db()
            query = "SELECT * FROM tasks WHERE 1=1"
            params = []

            if status and status in ['pending', 'completed']:
                query += " AND status = ?"
                params.append(status)

            if keyword:
                query += " AND (title LIKE ? OR description LIKE ?)"
                search_pattern = f"%{keyword.strip()}%"
                params.extend([search_pattern, search_pattern])

            query += " ORDER BY created_at DESC"
            
            cursor = db.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [cls.from_row(row) for row in rows]
        except sqlite3.Error as e:
            print(f"資料庫查詢任務列表失敗: {e}", file=sys.stderr)
            return []

    @classmethod
    def get_by_id(cls, task_id):
        """
        依據指定 ID 查詢單一任務。
        
        參數:
            task_id (int): 任務 ID
            
        回傳:
            Task: 查詢到的 Task 物件，若不存在或發生異常則回傳 None
        """
        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            row = cursor.fetchone()
            return cls.from_row(row)
        except sqlite3.Error as e:
            print(f"資料庫依 ID 查詢任務失敗: {e}", file=sys.stderr)
            return None

    @classmethod
    def update(cls, task_id, title, description=None):
        """
        修改指定 ID 任務的標題與描述。
        
        參數:
            task_id (int): 任務 ID
            title (str): 新任務標題
            description (str, optional): 新任務描述
            
        回傳:
            bool: 更新成功回傳 True，失敗或發生異常回傳 False
        """
        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                "UPDATE tasks SET title = ?, description = ? WHERE id = ?",
                (title.strip(), (description or '').strip(), task_id)
            )
            db.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"資料庫更新任務內容失敗: {e}", file=sys.stderr)
            return False

    @classmethod
    def update_status(cls, task_id, status):
        """
        修改指定 ID 任務的完成狀態。
        
        參數:
            task_id (int): 任務 ID
            status (str): 新狀態 ('pending' 或 'completed')
            
        回傳:
            bool: 狀態更新成功回傳 True，失敗或發生異常回傳 False
        """
        if status not in ['pending', 'completed']:
            raise ValueError("無效的任務狀態")
        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute(
                "UPDATE tasks SET status = ? WHERE id = ?",
                (status, task_id)
            )
            db.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"資料庫更新任務狀態失敗: {e}", file=sys.stderr)
            return False

    @classmethod
    def delete(cls, task_id):
        """
        依據指定 ID 刪除任務。
        
        參數:
            task_id (int): 任務 ID
            
        回傳:
            bool: 刪除成功回傳 True，失敗或發生異常回傳 False
        """
        try:
            db = get_db()
            cursor = db.cursor()
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            db.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"資料庫刪除任務失敗: {e}", file=sys.stderr)
            return False
