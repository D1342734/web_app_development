from app import create_app

# 建立 Flask 應用程式實例
app = create_app()

if __name__ == '__main__':
    # 在本地端啟動開發伺服器，預設連接埠為 5000，啟用 Debug 模式以利除錯
    app.run(debug=True)
