#app.py
import pymysql
from flask import Flask, request, jsonify, g
from flask_cors import CORS
import database
from os import path
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
app.config["JWT_SECRET_KEY"] = "super-secret"
UPLOAD_FOLDER = path.join('.', 'resources/')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
jwt = JWTManager(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
# OPTIONS 메서드 처리를 위한 라우트

#인식못할때 라우팅
@app.route('/company_undefined/user', methods=['GET', 'OPTIONS'])
def get_user_data():
    if request.method == 'OPTIONS':
        return '', 200  # OPTIONS 메서드에 대한 응답
    try:
        with pymysql.connect(**database.connectionString) as con:
            cursor = con.cursor()
            # 현재 사용자의 스키마로 전환
            user_schema = f"company_{g.company_id}"
            cursor.execute(f"USE {user_schema};")
            # 사용자 정보 조회 쿼리
            sql = "SELECT * FROM user;"
            cursor.execute(sql)
            user_data = cursor.fetchall()

            return jsonify({'users': user_data})

    except Exception as e:
        print("Error fetching user data:", e)
        return jsonify({"message": "Error fetching user data"}), 500


@app.route('/company/user', methods=['GET'])
def get_user_data_by_company_id():
    try:
        # 클라이언트에서 보낸 Company-ID를 헤더에서 읽어옴
        company_id = request.headers.get('Company-ID')

        # Company-ID가 None이면 디폴트 값으로 설정
        if company_id is None:
            company_id = 'default_company_id'

        with pymysql.connect(**database.connectionString) as con:
            cursor = con.cursor()

            # 현재 사용자의 스키마로 전환
            user_schema = f"company_{company_id}"
            cursor.execute(f"USE {user_schema};")

            # 사용자 정보 조회 쿼리
            sql = "SELECT * FROM user;"
            cursor.execute(sql)
            user_data = cursor.fetchall()

            return jsonify({'users': user_data})

    except Exception as e:
        print("Error fetching user data:", e)
        return jsonify({"message": "Error fetching user data"}), 500

@app.before_request
def before_request():
    # 요청이 들어올 때마다 헤더에서 'Company-ID'를 읽어서 g 객체에 저장
    g.company_id = request.headers.get('Company-ID')
# g.company_id가 None이면 오류를 방지하기 위해 기본값으로 설정
    if g.company_id is None:
        g.company_id = '69'
@app.route('/', methods=['GET'])
def main():
    sort = request.args.get('sort')
    keyword = request.args.get('keyword')
    return database.getItems(sort, keyword)

@app.route('/rowadmin', methods=['GET'])
def admin_page():
    try:
        with pymysql.connect(**database.connectionString) as con:
            cursor = con.cursor()
            # 현재 사용자의 스키마로 전환
            user_schema = f"company_{g.company_id}"
            cursor.execute(f"USE {user_schema};")
            # 사용자 정보 조회 쿼리
            sql = "SELECT * FROM user;"
            cursor.execute(sql)
            user_data = cursor.fetchall()

            return jsonify({'users': user_data})

    except Exception as e:
        print("Error fetching user data:", e)
        return jsonify({"message": "Error fetching user data"}), 500

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

@app.route('/login', methods=["POST"])
def login():
    if request.method == 'POST':
        userId = request.json.get('email')
        password = request.json.get('password')

        user_info, company_id = database.get_user_info_and_company_id(userId, password)

        if user_info and company_id:
            with pymysql.connect(**database.connectionString) as con:
                cursor = con.cursor()
                schema_name = f"company_{company_id}"
                cursor.execute(f"USE {schema_name};")

            # 응답에 'company_id' 포함
            response = {
                'token': create_access_token(identity=userId),
                'userId': userId,
                'company_id': company_id
            }
            return jsonify(response), 200

        return jsonify({'message': '잘못된 로그인 정보입니다. 다시 입력해주세요.'}), 401

# 회원가입페이지
@app.route('/login/signup', methods=['POST'])
def signup():
    try:
        print("-------------------------------------------------")
        # 클라이언트로부터의 요청에서 필요한 정보 추출
        userId = request.json.get('userId')
        userPwd = request.json.get('userPwd')
        name = request.json.get('name')  # 추가
        phone = request.json.get('phone')  # 추가
        start_date = request.json.get('start_date')  # 추가
        industryCategory = request.json.get('industryCategory')  # 추가
        isSubscribed = request.json.get('isSubscribed')  # 추가

        print(f"Received data: userId={userId}, userPwd={userPwd}, name={name}, phone={phone}, start_date={start_date}, industryCategory={industryCategory}, isSubscribed={isSubscribed}")

        # 사용자 정보를 데이터베이스에 추가하고 결과를 받아옴
        userInfo, status_code, headers = database.addUserInfo(userId, userPwd, name, phone, start_date, industryCategory, isSubscribed)
        print(f"Database response: {userInfo}")

        # 사용자 정보가 성공적으로 추가되면 JWT 토큰 생성
        access_token = create_access_token(identity=userId)
        print(f"Generated access token: {access_token}")

        return jsonify({"message": "계정 추가 및 로그인 성공", "token": access_token, 'userId': userId}), 200, {
            'Content-Type': 'application/json'}

    except Exception as e:
        print(f"Error in signup: {e}")
        return jsonify({"message": "요청중 에러가 발생"}), 500, {'Content-Type': 'application/json'}

# if __name__ == "__main__":
#     app.run(debug = True)
if __name__ == "__main__":
    app.run(host='0.0.0.0')