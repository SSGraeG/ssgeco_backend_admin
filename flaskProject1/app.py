from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token
import database
import os

# Flask 애플리케이션 초기화
app = Flask(__name__, static_folder='./resources/')
CORS(app)
# JWT 설정
app.config["JWT_SECRET_KEY"] = "super-secret"
UPLOAD_FOLDER = os.path.join('.', 'resources/')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
jwt = JWTManager(app)

# CORS 설정
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# 메인 페이지
@app.route('/', methods=['GET'])
def main():
    sort = request.args.get('sort')
    keyword = request.args.get('keyword')
    return database.getItems(sort, keyword, "editor", "editor2")

# 고객 데이터 API
@app.route('/api/get_data', methods=['GET'])
def get_customer_data():
    return database.get_customer_data("editor", "editor2")

# 차트 데이터 API
@app.route('/api/getChartData/<usernum>', methods=['GET'])
def get_chart_data(usernum):
    chart_data = {'usernum': usernum, 'chart': 'data'}
    return jsonify(chart_data)

# 로그인 API
@app.route('/login', methods=["POST"])
def login():
    if request.method == 'POST':
        userId = request.json.get('email')
        password = request.json.get('password')

        # idCheck 함수로 로그인 확인
        isid = database.idCheck(userId, password, "editor", "editor2")
        if isid:
            access_token = create_access_token(identity=userId)
            return jsonify({'token': access_token, 'userId': userId}), 200
        else:
            return jsonify({'message': '잘못된 로그인 정보입니다. 다시 입력해주세요.'}), 401

# 회원가입 API
@app.route('/login/signup', methods=['POST'])
def signup():
    try:
        userId = request.json.get('userId')
        userPwd = request.json.get('userPwd1')
        selectedSchema = request.json.get('selectedSchema', 'editor')  # 기본값은 'editor'

        # 아래의 함수에서 스키마 정보를 사용하여 작업을 수행하면 됩니다.
        userInfo, status_code, headers = database.addUserInfo(userId, userPwd, selectedSchema)

        access_token = create_access_token(identity=userId)
        return jsonify({"message": "계정 추가 및 로그인 성공", "token": access_token, 'userId': userId}), 200, {
            'Content-Type': 'application/json'}

    except Exception as e:
        print(e)
        return jsonify({"message": "요청중 에러가 발생"}), 500, {'Content-Type': 'application/json'}
# 애플리케이션 실행
if __name__ == "__main__":
    app.run(host='0.0.0.0')
