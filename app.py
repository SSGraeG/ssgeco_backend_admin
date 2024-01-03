# app.py

from flask import Flask, request, g
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from os import path
from route import database
from route.user import user_bp
from route.manage import manage_bp
from route.chart import chart_bp
from route.admin import admin_bp

def create_app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "super-secret"
    UPLOAD_FOLDER = path.join('flaskProject1', 'resources/')
    jwt = JWTManager(app)
    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    # Blueprint 등록
    app.register_blueprint(user_bp)
    app.register_blueprint(manage_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(chart_bp)

    @app.route('/', methods=['GET'])
    def main():
        sort = request.args.get('sort')
        keyword = request.args.get('keyword')
        return database.getItems(sort, keyword)

    @app.route('/test')
    def test():
        return "test"

    @app.before_request
    def before_request():
        # 요청이 들어올 때마다 헤더에서 'Company-ID'를 읽어서 g 객체에 저장
        g.company_id = request.headers.get('Company-ID')
        # g.company_id가 None이면 오류를 방지하기 위해 기본값으로 설정
        if g.company_id is None:
            g.company_id = '69'

    return app

if __name__ == '__main__':
    create_app().run(debug=True, host='0.0.0.0', port=5000)
