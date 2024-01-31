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

        # Terraform 파일을 적용
        terraform_dir = '/path/to/terraform/directory'  # Terraform이 실행될 디렉토리
        terraform_file = 'new-vpc.tf'  # Terraform 구성 파일명

        # new-vpc.tf 파일이 존재하는지 확인
        if os.path.exists(os.path.join(terraform_dir, terraform_file)):
            # Terraform init 명령 실행
            subprocess.run("terraform init -auto-approve", shell=True, cwd=terraform_dir)

            # Terraform apply 명령 실행
            subprocess.run("terraform apply -auto-approve", shell=True, cwd=terraform_dir)

            return jsonify({"message": "계정 추가 및 로그인 성공", "token": access_token, 'userId': userId}), 200, {
                'Content-Type': 'application/json'}
        else:
            return jsonify({"message": "Terraform 구성 파일이 존재하지 않습니다."}), 500, {'Content-Type': 'application/json'}

    except Exception as e:
        print(f"Error in signup: {e}")
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

        # Terraform 파일을 적용
        terraform_dir = 'ssgadminBE/route'  # Terraform이 실행될 디렉토리
        terraform_file = 'new-vpc.tf'  # Terraform 구성 파일명

        # new-vpc.tf 파일이 존재하는지 확인
        if os.path.exists(os.path.join(terraform_dir, terraform_file)):
            # Terraform init 명령 실행
            subprocess.run("terraform init -auto-approve", shell=True, cwd=terraform_dir)

            # Terraform apply 명령 실행
            subprocess.run("terraform apply -auto-approve", shell=True, cwd=terraform_dir)

            return jsonify({"message": "계정 추가 및 로그인 성공", "token": access_token, 'userId': userId}), 200, {
                'Content-Type': 'application/json'}
        else:
            return jsonify({"message": "Terraform 구성 파일이 존재하지 않습니다."}), 500, {'Content-Type': 'application/json'}

    except Exception as e:
        print(f"Error in signup: {e}")
        return jsonify({"message": "요청중 에러가 발생"}), 500, {'Content-Type': 'application/json'}