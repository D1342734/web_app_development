# 路由與頁面設計文件 (Routes & Page Design) - 任務管理系統

本文件規劃「任務管理系統」的 Flask 路由路徑、HTTP 請求方法、輸入輸出規範、Jinja2 模板結構以及對應的程式碼骨架。

---

## 1. 路由總覽表格

本系統之路由設計遵循 RESTful 風格，由於使用原生 HTML 表單限制，更新與刪除操作將使用 `POST` 方法處理。

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 (View) | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **首頁 / 任務列表** | `GET` | `/` | `app/templates/index.html` | 展示任務清單，支援依關鍵字搜尋與完成狀態篩選。 |
| **新增任務** | `POST` | `/tasks/add` | *(重導向至 `/`)* | 接收主頁面提交之新增表單，存入資料庫後跳轉回首頁。 |
| **編輯任務頁面** | `GET` | `/tasks/<int:task_id>/edit` | `app/templates/edit.html` | 讀取指定 ID 的任務資料並顯示編輯表單。 |
| **更新任務內容** | `POST` | `/tasks/<int:task_id>/edit` | *(重導向至 `/`)* | 接收編輯表單之提交，更新資料庫後跳轉回首頁。 |
| **刪除任務** | `POST` | `/tasks/<int:task_id>/delete`| *(重導向至 `/`)* | 接收刪除表單之提交，將指定任務物理刪除後跳轉回首頁。 |
| **切換任務狀態** | `POST` | `/tasks/<int:task_id>/toggle`| *(回傳 JSON)* | 供 JavaScript fetch 非同步呼叫，變更完成狀態後回傳狀態 JSON。 |

---

## 2. 每個路由的詳細說明

### 2.1. 顯示首頁 (`GET /`)
*   **輸入**：
    *   Query 參數 `status`：選填。篩選值可為 `all`、`pending`（未完成）、`completed`（已完成）。
    *   Query 參數 `keyword`：選填。搜尋之關鍵字，比對標題與內容。
*   **處理邏輯**：
    *   呼叫 `Task.get_all(status=status, keyword=keyword)` 讀取資料。
*   **輸出**：
    *   成功：渲染並回傳 `index.html` 網頁，傳入 `tasks` 串列、目前的 `status` 與 `keyword` 供頁面狀態回顯。
*   **錯誤處理**：
    *   無相符任務時，渲染 `index.html`，但傳遞空串列，並在前端提示「查無相關任務」。

### 2.2. 新增任務 (`POST /tasks/add`)
*   **輸入**：
    *   表單欄位 `title`：必填，最多 100 字。
    *   表單欄位 `description`：選填，最多 500 字。
*   **處理邏輯**：
    *   檢查 `title` 是否為空。
    *   若檢查通過，呼叫 `Task.create(title, description)` 寫入資料庫。
*   **輸出**：
    *   成功：HTTP 302 重導向至 `url_for('main.index')`。
    *   資料驗證失敗：渲染首頁並附帶錯誤訊息（或重導向至首頁並帶閃現訊息 Flash Message）。

### 2.3. 編輯任務頁面與更新 (`GET & POST /tasks/<int:task_id>/edit`)
*   **GET 請求**：
    *   **處理邏輯**：呼叫 `Task.get_by_id(task_id)`。
    *   **輸出**：成功渲染 `edit.html` 並傳入 `task` 物件；若任務不存在，則拋出 404 錯誤。
*   **POST 請求**：
    *   **輸入**：表單欄位 `title` (必填) 與 `description` (選填)。
    *   **處理邏輯**：檢查 `title` 是否為空。若合法，呼叫 `Task.update(task_id, title, description)`。
    *   **輸出**：成功後 HTTP 302 重導向至 `url_for('main.index')`。

### 2.4. 刪除任務 (`POST /tasks/<int:task_id>/delete`)
*   **輸入**：無（由 URL 路徑指定 `task_id`）。
*   **處理邏輯**：呼叫 `Task.delete(task_id)`。
*   **輸出**：成功後 HTTP 302 重導向至 `url_for('main.index')`。若該任務不存在，則拋出 404 錯誤。

### 2.5. 切換任務狀態 (`POST /tasks/<int:task_id>/toggle`)
*   **輸入**：無（由 URL 路徑指定 `task_id`，非同步發送）。
*   **處理邏輯**：
    1. 呼叫 `Task.get_by_id(task_id)`。
    2. 依現有狀態，呼叫 `Task.update_status(task_id, 'completed' / 'pending')` 進行狀態切換。
*   **輸出**：
    *   成功：回傳 JSON `{ "success": True, "new_status": "completed" / "pending" }`。
    *   失敗：回傳 JSON `{ "success": False, "error": "Task not found" }`，並帶有 HTTP 404 狀態碼。

---

## 3. Jinja2 模板清單

系統頁面由以下 HTML 模板構成，皆位於 `app/templates/` 目錄：

1.  **[base.html](file:///c:/Users/user/Downloads/新增資料夾 (2)/新增資料夾/web_app_development/app/templates/base.html)**：
    *   **用途**：最基礎的母版 (Base Layout)。
    *   **內容**：包含 HTML 宣告、`<head>`（載入 Google Fonts、`style.css`）、全域導覽列 (Navigation Bar)、放動態內容的 `{% block content %}`，以及載入 `main.js` 的區塊。
2.  **[index.html](file:///c:/Users/user/Downloads/新增資料夾 (2)/新增資料夾/web_app_development/app/templates/index.html)**：
    *   **用途**：首頁暨任務管理主畫面。
    *   **繼承**：`base.html`。
    *   **內容**：
        *   頂部的搜尋欄（Search Box）。
        *   新增任務表單（Inline Form）。
        *   篩選標籤按鈕（All / Pending / Completed）。
        *   任務清單列表（Task List），使用 `{% for task in tasks %}` 渲染每一項任務，包含 Checkbox、編輯按鈕及刪除表單。
3.  **[edit.html](file:///c:/Users/user/Downloads/新增資料夾 (2)/新增資料夾/web_app_development/app/templates/edit.html)**：
    *   **用途**：編輯任務專屬頁面。
    *   **繼承**：`base.html`。
    *   **內容**：顯示該任務的編輯表單，預先帶入舊的標題與內容，包含「儲存更新」與「取消並回首頁」按鈕。

---

## 4. 路由骨架程式碼預覽

路由骨架實作於 [main.py](file:///c:/Users/user/Downloads/新增資料夾 (2)/新增資料夾/web_app_development/app/routes/main.py) 中。
