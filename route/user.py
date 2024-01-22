import pymysql
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from . import database

user_bp = Blueprint('user', __name__)

@user_bp.route('/')
def test_route():
    return jsonify({'test': 'V2'}), 200

@user_bp.route('/login', methods=["POST"])
def login():
    if request.method == 'POST':
        userId = request.json.get('email')
        password = request.json.get('password')

        user_info, company_id, role = database.get_user_info_and_company_id_and_role(userId, password)

        if user_info and company_id:
            with pymysql.connect(**database.connectionString) as con:
                cursor = con.cursor()
                schema_name = f"company_{company_id}"
                cursor.execute(f"USE {schema_name};")

            # 응답에 'company_id'와 'role' 포함
            response = {
                'token': create_access_token(identity=userId),
                'userId': userId,
                'company_id': company_id,
                'role': role
            }

            # role이 1이면 /admin에 대한 접근 권한을 확인하도록 설정
            if role == 1:
                response['can_access_admin'] = True
                response['can_access_admin2'] = True
            else:
                response['can_access_admin'] = False
                response['can_access_admin2'] = False
            return jsonify(response), 200
        return jsonify({'message': '잘못된 로그인 정보입니다. 다시 입력해주세요.'}), 401

@user_bp.route('/login/signup', methods=['POST'])
def signup():
    try:
        # 클라이언트로부터의 요청에서 필요한 정보 추출
        userId = request.json.get('userId')
        userPwd = request.json.get('userPwd')
        name = request.json.get('name')
        phone = request.json.get('phone')
        start_date = request.json.get('start_date')
        category = request.json.get('category')  # 수정
        aiCategory = request.json.get('aiCategory')  # 수정
        infraCategory = request.json.get('infraCategory')  # 수정
        isSubscribed = request.json.get('isSubscribed')

        print(
            f"Received data: userId={userId}, userPwd={userPwd}, name={name}, phone={phone}, start_date={start_date},category={category}, aiCategory={aiCategory}, infraCategory={infraCategory}, isSubscribed={isSubscribed}")

        # 사용자 정보를 데이터베이스에 추가하고 결과를 받아옴
        userInfo, status_code, headers = database.addUserInfo(userId, userPwd, name, phone, start_date, category, aiCategory,
                                                              infraCategory, isSubscribed)
        print(f"Database response: {userInfo}")

        # 사용자 정보가 성공적으로 추가되면 JWT 토큰 생성
        access_token = create_access_token(identity=userId)
        print(f"Generated access token: {access_token}")

        return jsonify({"message": "계정 추가 및 로그인 성공", "token": access_token, 'userId': userId}), 200, {
            'Content-Type': 'application/json'}
    except Exception as e:
        print(f"Error in signup: {e}")
        return jsonify({"message": "요청중 에러가 발생"}), 500, {'Content-Type': 'application/json'}
