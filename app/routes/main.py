from flask import Blueprint, render_template, request, redirect, url_for, jsonify

# 建立 Blueprint 實例，用於將此模組的路由註冊到 Flask App
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """
    顯示首頁與任務列表。
    
    支援以下 Query Strings:
    - status: 篩選完成狀態 ('all', 'pending', 'completed')
    - keyword: 搜尋關鍵字 (針對 title 與 description)
    
    回傳:
        index.html 模板渲染的網頁內容
    """
    # 骨架暫留，待實作階段填入邏輯
    pass

@main_bp.route('/tasks/add', methods=['POST'])
def add_task():
    """
    接收新增任務表單的 POST 請求。
    
    欄位:
    - title: 任務標題 (必填)
    - description: 任務描述 (選填)
    
    回傳:
        儲存完成後，HTTP 302 重導向回首頁 (/)
    """
    # 骨架暫留，待實作階段填入邏輯
    pass

@main_bp.route('/tasks/<int:task_id>/edit', methods=['GET', 'POST'])
def edit_task(task_id):
    """
    GET: 顯示特定任務的編輯表單頁面 (edit.html)
    POST: 接收編輯表單的提交，更新任務內容
    
    參數:
    - task_id: 任務的主鍵 ID
    
    回傳:
        GET: edit.html 模板渲染的網頁內容
        POST: 更新完成後，HTTP 302 重導向回首頁 (/)
    """
    # 骨架暫留，待實作階段填入邏輯
    pass

@main_bp.route('/tasks/<int:task_id>/delete', methods=['POST'])
def delete_task(task_id):
    """
    刪除指定的任務。
    
    參數:
    - task_id: 任務的主鍵 ID
    
    回傳:
        刪除完成後，HTTP 302 重導向回首頁 (/)
    """
    # 骨架暫留，待實作階段填入邏輯
    pass

@main_bp.route('/tasks/<int:task_id>/toggle', methods=['POST'])
def toggle_task(task_id):
    """
    切換任務的完成狀態 (pending <-> completed)。
    此路由專供前端 JavaScript 以 fetch API 非同步呼叫。
    
    參數:
    - task_id: 任務的主鍵 ID
    
    回傳:
        JSON 格式回饋:
        - 成功: { "success": true, "new_status": "completed" / "pending" }
        - 失敗: { "success": false, "error": "錯誤原因" }, 狀態碼 404/400
    """
    # 骨架暫留，待實作階段填入邏輯
    pass
