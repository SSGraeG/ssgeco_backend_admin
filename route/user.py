import pymysql
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from . import database
import subprocess
import os

user_bp = Blueprint('user', __name__)

@user_bp.route('/test')
def test_route():
    return jsonify({'test': 'succeed'}), 200

@user_bp.route('/login', methods=["POST"])
def login():
    try:
        if request.method == 'POST':
            userId = request.json.get('email')
            password = request.json.get('password')

            user_info, company_id, role, subscription_status, infraCategory = database.get_user_info_and_company_id_and_role(userId, password)

            if user_info and company_id:
                with pymysql.connect(**database.connectionString) as con:
                    cursor = con.cursor()
                    schema_name = f"company_{company_id}"
                    cursor.execute(f"USE {schema_name};")

                # 응답에 'company_id', 'role', 'subscription_status'를 포함
                response = {
                    'token': create_access_token(identity=userId),
                    'userId': userId,
                    'company_id': company_id,
                    'role': role,
                    'subscription_status': subscription_status,
                    'infraCategory': infraCategory
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

    except Exception as e:
        print(f"Error in login: {e}")
        return jsonify({"message": "요청중 에러가 발생"}), 500, {'Content-Type': 'application/json'}
@user_bp.route('/login/signup', methods=['POST'])
def signup():
    try:
        # 클라이언트로부터의 요청에서 필요한 정보 추출
        userId = request.json.get('userId')
        userPwd = request.json.get('userPwd')
        name = request.json.get('name')
        phone = request.json.get('phone')
        start_date = request.json.get('start_date')
        category = request.json.get('category')
        aiCategory = request.json.get('aiCategory')
        infraCategory = request.json.get('infraCategory')
        isSubscribed = request.json.get('isSubscribed')

        print(
            f"Received data: userId={userId}, userPwd={userPwd}, name={name}, phone={phone}, start_date={start_date},category={category}, aiCategory={aiCategory}, infraCategory={infraCategory}, isSubscribed={isSubscribed}")

        # 사용자 정보를 데이터베이스에 추가하고 결과를 받아옴
        userInfo, status_code, headers = database.addUserInfo(userId, userPwd, name, phone, start_date, category,
                                                              aiCategory,
                                                              infraCategory, isSubscribed)
        print(f"Database response: {userInfo}")

        # 사용자 정보가 성공적으로 추가되면 JWT 토큰 생성
        access_token = create_access_token(identity=userId)
        print(f"Generated access token: {access_token}")

        # 회원가입 성공 메시지 전송
        success_message = {"message": "계정 추가 및 로그인 성공", "token": access_token, 'userId': userId}
        return jsonify(success_message), 200, {'Content-Type': 'application/json'}

        # Terraform 파일을 적용
        terraform_dir = '/home/ubuntu'  # Terraform이 실행될 디렉토리
        terraform_file = 'new-user.tf'  # Terraform 구성 파일명

        # new-vpc.tf 파일이 존재하는지 확인
        if os.path.exists(os.path.join(terraform_dir, terraform_file)):
            # Terraform init 명령 실행
            subprocess.run("terraform init -auto-approve", shell=True, cwd=terraform_dir)

            # Terraform apply 명령 실행
            terraform_apply_result = subprocess.run("terraform apply -auto-approve", shell=True, cwd=terraform_dir)

            # Terraform apply가 성공적으로 실행되었을 때만 추가 메시지 전송
            if terraform_apply_result.returncode == 0:
                additional_message = {"message": "Terraform apply 성공"}
            else:
                additional_message = {"message": "Terraform apply 중 에러가 발생하였습니다."}
        else:
            additional_message = {"message": "Terraform 구성 파일이 존재하지 않습니다."}

        return jsonify(additional_message), 200, {'Content-Type': 'application/json'}

    except Exception as e:
        print(f"Error in signup: {e}")
        return jsonify({"message": "요청중 에러가 발생"}), 500, {'Content-Type': 'application/json'}
