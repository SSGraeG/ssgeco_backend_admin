from datetime import datetime, timedelta
import pymysql
import os

from flask import jsonify
from pymysql import connect

# 데이터베이스 연결 설정
connectionString = {
    'host': 'eco-rds.chjhms6dyeyt.ap-northeast-1.rds.amazonaws.com',
    'port': 3306,  # 예시 포트, 실제 포트에 맞게 수정
    'database': 'eco',
    'user': 'admin',
    'password': 'password',
    'charset': 'utf8',
    'cursorclass': pymysql.cursors.DictCursor
}

def getItems(sort, keyword):
    try:
        # 기본 정렬 열을 설정 (실제 테이블의 컬럼으로 설정)
        default_sort = 'usernum'

        # sort 값이 None이면 기본 정렬 열로 설정
        sort = sort or default_sort

        # keyword 값이 None이면 빈 문자열로 설정
        keyword = keyword or ''

        with connect(**connectionString) as con:
            cursor = con.cursor()
            # 예시 쿼리 (실제 데이터베이스 쿼리에 맞게 수정해야 함)
            sql = f"SELECT * FROM eco.customer WHERE eco.customer.usersnum = '{keyword}' ORDER BY {sort};"
            cursor.execute(sql)
            result = cursor.fetchall()

            return jsonify({'data': result})

    except Exception as e:
        print(f"Error in getItems: {e}")
        return jsonify({"message": "고객 데이터를 가져오는 중 오류가 발생했습니다."}), 500




# 테이블 생성 쿼리 파일 경로
queries_file_path = os.path.join(os.path.dirname(__file__), 'queries.sql')
# queries.sql 파일을 읽어와 쿼리를 문자열로 저장
with open(queries_file_path, 'r') as queries_file:
    create_tables_query = queries_file.read()

def get_customer_data():
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()
            sql = "SELECT * FROM customer;"
            cursor.execute(sql)
            customer_data = cursor.fetchall()

            # Exclude the first record from the list
            modified_customer_data = customer_data[1:]

            return jsonify({'users': modified_customer_data})

    except Exception as e:
        print(f"Error in get_customer_data: {e}")
        return jsonify({"message": "고객 데이터를 가져오는 중 오류가 발생했습니다."}), 500

def idCheck(user_id, pwd):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()
            sql = "SELECT * FROM customer WHERE email = %s AND password = %s;"
            cursor.execute(sql, [user_id, pwd])
            result = cursor.fetchall()

            return result
    except Exception as e:
        print(f"Error in idCheck: {e}")

def addUserInfo(userId, userPwd, name, phone, start_date,category, aiCategory, infraCategory, isSubscribed):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()

            # 구독 여부를 'yes' 또는 'no'로 변환
            subscription_status = 'yes' if isSubscribed else 'no'

            # 만료 날짜 계산: 1년 후
            start_date_object = datetime.strptime(start_date, '%Y-%m-%d')
            expiration_date_object = start_date_object + timedelta(days=365)
            expiration_date = expiration_date_object.strftime('%Y-%m-%d')

            # 회원 정보를 customer 테이블에 추가
            sql = """
                INSERT INTO customer (email, password, company_name, phone, start_date,category, aiCategory, infraCategory, subscription_status, end_date)
                VALUES (%s, %s, %s,%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                userId, userPwd, name, phone, start_date,category, aiCategory, infraCategory, subscription_status, expiration_date))
            con.commit()

            # 새로운 스키마 생성
            cursor.execute("SELECT LAST_INSERT_ID() AS last_id;")
            result = cursor.fetchone()

            if result and 'last_id' in result:
                last_row_id = result['last_id']

                # 새로운 스키마 생성 쿼리
                new_schema_name = f"company_{last_row_id}"
                create_schema_query = f"CREATE DATABASE IF NOT EXISTS {new_schema_name};"
                cursor.execute(create_schema_query)

                # 새로운 스키마로 전환
                cursor.execute(f"USE {new_schema_name};")

                # 여러 쿼리를 ; 으로 분리하여 리스트에 담기
                queries = [query.strip() for query in create_tables_query.split(';') if query.strip()]

                # 각 쿼리를 실행
                for query in queries:
                    cursor.execute(query)

                return jsonify({"message": "사용자 정보가 성공적으로 추가되었으며, 새로운 스키마가 생성되었습니다."}), 200, {
                    'Content-Type': 'application/json'}

            else:
                return jsonify({"message": "마지막 삽입된 ID를 가져오는 중 오류가 발생했습니다."}), 500, {'Content-Type': 'application/json'}

    except Exception as e:
        print(e)
        return jsonify({"message": "사용자 정보를 추가하는 중 오류가 발생했습니다."}), 500, {'Content-Type': 'application/json'}

def get_user_info_and_company_id_and_role(user_id, pwd):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()
            sql = "SELECT email, company_id, role FROM customer WHERE email = %s AND password = %s;"
            cursor.execute(sql, [user_id, pwd])
            result = cursor.fetchone()

            if result:
                user_info = {'email': result['email']}
                company_id = result['company_id']
                role = result['role']
                return user_info, company_id, role

            return None, None, None

    except Exception as e:
        print(f"Error in get_user_info_and_company_id_and_role: {e}")
        return None, None, None

