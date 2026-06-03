/**
 * TaskFlow 前端互動設計腳本 (Client-Side Interactivity)
 */

document.addEventListener('DOMContentLoaded', () => {
    // 註冊非同步狀態切換監聽器
    initTaskToggleListeners();
    
    // 初始化 Bootstrap 表單驗證機制
    initFormValidation();
});

/**
 * 註冊任務 Checkbox 切換完成狀態的非同步監聽器
 */
function initTaskToggleListeners() {
    const checkboxes = document.querySelectorAll('.task-toggle-checkbox');
    
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', async (event) => {
            const taskId = event.target.dataset.taskId;
            const isChecked = event.target.checked;
            
            // 鎖定 Checkbox，防範重複連點
            event.target.disabled = true;
            
            try {
                // 發送 POST 請求非同步修改任務狀態
                const response = await fetch(`/tasks/${taskId}/toggle`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                });
                
                const data = await response.json();
                
                if (response.ok && data.success) {
                    // 根據新狀態動態更新 UI 類別
                    updateTaskCardUI(taskId, data.new_status);
                } else {
                    // 發生錯誤時恢復 Checkbox 狀態並報錯
                    event.target.checked = !isChecked;
                    showToastAlert(data.error || '狀態更新失敗，請稍後再試。', 'error');
                }
            } catch (error) {
                // 網路或系統崩潰時恢復 Checkbox 狀態
                event.target.checked = !isChecked;
                showToastAlert('無法連接到伺服器，請檢查網路連線。', 'error');
                console.error('Error toggling task:', error);
            } finally {
                // 解除 Checkbox 鎖定
                event.target.disabled = false;
            }
        });
    });
}

/**
 * 根據最新狀態，動態微調任務卡片與標章的視覺效果
 * @param {string} taskId - 任務 ID
 * @param {string} status - 新狀態 ('completed' 或 'pending')
 */
function updateTaskCardUI(taskId, status) {
    const taskCard = document.getElementById(`task-card-${taskId}`);
    const statusBadge = document.getElementById(`task-badge-${taskId}`);
    
    if (!taskCard) return;
    
    if (status === 'completed') {
        // 套用已完成樣式
        taskCard.classList.add('task-completed');
        
        if (statusBadge) {
            statusBadge.textContent = '已完成';
            statusBadge.className = 'status-indicator-badge status-completed';
        }
    } else {
        // 套用待處理樣式
        taskCard.classList.remove('task-completed');
        
        if (statusBadge) {
            statusBadge.textContent = '待處理';
            statusBadge.className = 'status-indicator-badge status-pending';
        }
    }
}

/**
 * 刪除任務時的二次防呆確認視窗
 * @param {Event} event - 表單提交事件
 * @param {string} taskTitle - 任務標題
 */
function confirmDelete(event, taskTitle) {
    event.preventDefault(); // 先阻止表單送出
    
    const confirmMessage = `您確定要永久刪除任務「${taskTitle}」嗎？\n此操作無法撤銷。`;
    
    if (confirm(confirmMessage)) {
        // 使用者點選確認，送出表單
        event.target.submit();
        return true;
    }
    
    return false;
}

/**
 * 動態產生系統級的 Toast 彈窗警告
 * @param {string} message - 顯示內容
 * @param {string} type - 警示類型 ('success' 或 'error')
 */
function showToastAlert(message, type = 'success') {
    const mainContainer = document.querySelector('main.container');
    if (!mainContainer) return;
    
    // 尋找或建立通知容器
    let alertContainer = document.querySelector('.flash-messages-container');
    if (!alertContainer) {
        alertContainer = document.createElement('div');
        alertContainer.className = 'flash-messages-container';
        mainContainer.insertBefore(alertContainer, mainContainer.firstChild);
    }
    
    // 建立 Custom Alert 元素
    const alertDiv = document.createElement('div');
    const alertClass = type === 'error' ? 'alert-danger' : 'alert-success';
    const alertIcon = type === 'error' ? 'fa-circle-exclamation' : 'fa-circle-check';
    
    alertDiv.className = `alert alert-dismissible fade show custom-alert ${alertClass}`;
    alertDiv.setAttribute('role', 'alert');
    alertDiv.innerHTML = `
        <div class="d-flex align-items-center">
            <i class="fa-solid ${alertIcon} me-2 fs-5"></i>
            <span>${message}</span>
        </div>
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    alertContainer.appendChild(alertDiv);
    
    // 5 秒後自動淡出消失
    setTimeout(() => {
        const bsAlert = new bootstrap.Alert(alertDiv);
        bsAlert.close();
    }, 5000);
}

/**
 * 初始化 Bootstrap 5 表單的前端驗證機制 (防範空白標題送出)
 */
function initFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
}
