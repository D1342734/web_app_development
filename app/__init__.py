import os
import click
from flask import Flask
from app.db import close_db
from app.routes.main import main_bp

def create_app(test_config=None):
    """Flask 應用程式工廠函數"""
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev_secret_key',
        DATABASE=os.path.join(app.instance_path, 'database.db'),
    )

    if test_config is None:
        # 載入 instance 目錄下的 config.py 設定 (若存在)
        app.config.from_pyfile('config.py', silent=True)
    else:
        # 載入傳入的測試設定
        app.config.from_mapping(test_config)

    # 確保 instance 資料夾存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 註冊請求結束時關閉資料庫連線的處理程序
    app.teardown_appcontext(close_db)

    # 註冊 Flask CLI 指令: flask init-db
    @app.cli.command('init-db')
    def init_db_command():
        """清除現有資料並建立新資料表"""
        init_db_logic(app)
        click.echo('資料庫初始化成功！')

    # 註冊路由 Blueprint
    app.register_blueprint(main_bp)

    return app

def init_db_logic(app):
    """執行資料庫 schema 初始化邏輯"""
    from app.db import get_db
    with app.app_context():
        db = get_db()
        # 讀取專案下的 database/schema.sql 腳本
        schema_path = os.path.join(app.root_path, '..', 'database', 'schema.sql')
        schema_path = os.path.abspath(schema_path)
        with open(schema_path, 'r', encoding='utf-8') as f:
            db.executescript(f.read())

def init_db():
    """供外部指令直接執行初始化，例如：python -c "from app import init_db; init_db()" """
    app = create_app()
    init_db_logic(app)
    print("資料庫初始化完成！")
