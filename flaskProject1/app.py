#app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import database
from os import path, remove
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
import os

app = Flask(__name__, static_folder='./resources/')
app.config["JWT_SECRET_KEY"] = "super-secret"
UPLOAD_FOLDER = path.join('.', 'resources/')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
jwt = JWTManager(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.route('/', methods=['GET'])
def main():
    sort = request.args.get('sort')
    keyword = request.args.get('keyword')
    return database.getItems(sort, keyword)

@app.route('/api/get_data', methods=['GET'])
def get_customer_data():
    return database.get_customer_data()

@app.route('/api/getChartData/<usernum>', methods=['GET'])
def get_chart_data(usernum):
    # 여기에서 usernum을 기반으로 차트 데이터를 가져와서 응답합니다.
    # 사용자 번호에 따른 차트 데이터를 반환하도록 데이터베이스 조회 등을 수행합니다.
    # 예시: chart_data = get_chart_data_from_database(usernum)
    chart_data = {'usernum': usernum, 'chart': 'data'}
    return jsonify(chart_data)

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        userId = request.json.get('email')
        password = request.json.get('password')

        isid = database.idCheck(userId, password)
        if (isid):
            access_token = create_access_token(identity=userId)
            return jsonify({'token': access_token, 'userId': userId}), 200
        else:
            return jsonify({'message': '잘못된 로그인 정보입니다. 다시 입력해주세요.'}), 401


# 회원가입페이지
@app.route('/login/signup', methods=['POST'])
def signup():
    try:
        print("-------------------------------------------------")
        # 클라이언트로부터의 요청에서 필요한 정보 추출
        userId = request.json.get('userId')
        userPwd = request.json.get('userPwd1')
        # 사용자 정보를 데이터베이스에 추가하고 결과를 받아옴
        userInfo, status_code, headers = database.addUserInfo(userId, userPwd)
        # 사용자 정보가 성공적으로 추가되면 JWT 토큰 생성
        access_token = create_access_token(identity=userId)
        print(userPwd, userId)
        return jsonify({"message": "계정 추가 및 로그인 성공", "token": access_token, 'userId': userId}), 200, {
            'Content-Type': 'application/json'}

    except Exception as e:
        print(e)
        return jsonify({"message": "요청중 에러가 발생"}), 500, {'Content-Type': 'application/json'}

# if __name__ == "__main__":
#     app.run(debug = True)
if __name__ == "__main__":
    app.run(host='0.0.0.0')