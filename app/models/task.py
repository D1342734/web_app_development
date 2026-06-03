from app.db import get_db

class Task:
    def __init__(self, id, title, description, status, created_at):
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.created_at = created_at

    @staticmethod
    def from_row(row):
        """將 sqlite3.Row 物件轉換成 Task 實例"""
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
        """新增一筆任務到資料庫"""
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO tasks (title, description, status) VALUES (?, ?, 'pending')",
            (title.strip(), (description or '').strip())
        )
        db.commit()
        return cursor.lastrowid

    @classmethod
    def get_all(cls, status=None, keyword=None):
        """獲取所有任務，支援依狀態篩選與關鍵字搜尋，按建立時間由新到舊排序"""
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

    @classmethod
    def get_by_id(cls, task_id):
        """依 ID 查詢單一任務"""
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        return cls.from_row(row)

    @classmethod
    def update(cls, task_id, title, description=None):
        """修改任務的標題與描述"""
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "UPDATE tasks SET title = ?, description = ? WHERE id = ?",
            (title.strip(), (description or '').strip(), task_id)
        )
        db.commit()
        return cursor.rowcount > 0

    @classmethod
    def update_status(cls, task_id, status):
        """變更任務完成狀態 (pending / completed)"""
        if status not in ['pending', 'completed']:
            raise ValueError("無效的任務狀態")
        db = get_db()
        cursor = db.cursor()
        cursor.execute(
            "UPDATE tasks SET status = ? WHERE id = ?",
            (status, task_id)
        )
        db.commit()
        return cursor.rowcount > 0

    @classmethod
    def delete(cls, task_id):
        """依 ID 刪除任務"""
        db = get_db()
        cursor = db.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        db.commit()
        return cursor.rowcount > 0
