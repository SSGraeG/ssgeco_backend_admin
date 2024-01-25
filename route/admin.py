import pymysql
from flask import Blueprint, jsonify, g
from . import database

admin_bp = Blueprint('admin', __name__)

def switch_to_company_schema(company_id, cursor):
    try:
        # 스키마 이름 생성 (예: company_1)
        schema_name = f"company_{company_id}"

        # 현재 스키마로 전환
        cursor.execute(f"USE {schema_name};")
        print(f"Switched to schema: {schema_name}")  # 로그 추가

    except Exception as e:
        print(f"Error switching to company schema: {e}")
        raise
@admin_bp.route('/admin', methods=['GET'])
def admin_page():
    try:
        with pymysql.connect(**database.connectionString) as con:
            cursor = con.cursor()

            # 모든 기업 정보 조회
            sql = "SELECT * FROM customer;"
            cursor.execute(sql)
            companies = cursor.fetchall()

            # 각 기업의 유저 수 조회
            company_user_counts = {}
            for company in companies:
                # 해당 기업의 스키마로 전환
                switch_to_company_schema(company['company_id'], cursor)

                # 사용자 수 조회 쿼리
                user_count_sql = "SELECT COUNT(*) AS user_count FROM user;"
                cursor.execute(user_count_sql)
                user_count = cursor.fetchone()['user_count']

                # 기업 아이디를 키로 사용하여 유저 수 저장
                company_user_counts[str(company['company_id'])] = user_count
            return jsonify({'companies': companies, 'user_counts': company_user_counts})

    except Exception as e:
        print("기업 데이터를 가져오는 중 오류:", e)
        return jsonify({"message": "기업 데이터를 가져오는 중 오류가 발생했습니다."}), 500

@admin_bp.route('/editor/customer/<email>', methods=['DELETE'])
def delete_customer(email):
    try:
        with pymysql.connect(**database.connectionString) as con:
            cursor = con.cursor()

            # 스키마 변경
            cursor.execute("USE eco;")

            # 테이블명 가져오기
            table_name = 'customer'

            # 사용자 삭제
            sql = f"DELETE FROM {table_name} WHERE email = %s;"
            cursor.execute(sql, (email,))
            con.commit()

            return jsonify({"message": f"사용자 {email}이(가) 성공적으로 삭제되었습니다."}), 200
    except Exception as e:
        print("사용자 삭제 중 오류 발생:", e)
        return jsonify({"message": "사용자 삭제 중 오류가 발생했습니다."}), 500

@admin_bp.route('/admin2', methods=['GET'])
def admin_page2():
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


@admin_bp.route('/rowadmin', methods=['GET'])
def rowadmin_page():
    try:
        with pymysql.connect(**database.connectionString) as con:
            cursor = con.cursor()

            # 현재 사용자의 스키마로 전환
            user_schema = f"company_{g.company_id}"
            cursor.execute(f"USE {user_schema};")


            # 사용자 정보 조회 쿼리
            sql_user = "SELECT * FROM user;"
            cursor.execute(sql_user)
            user_data = cursor.fetchall()

            # 마일리지 추적 정보 조회 쿼리
            sql_mileage_tracking = """
                SELECT * FROM mileage_tracking
                INNER JOIN mileage_category ON mileage_tracking.mileage_category_id = mileage_category.id;
            """
            cursor.execute(sql_mileage_tracking)
            mileage_tracking_data = cursor.fetchall()

            return jsonify({'users': user_data, 'mileage_tracking': mileage_tracking_data})

    except Exception as e:
        print("Error fetching user and mileage tracking data:", e)
        return jsonify({"message": "Error fetching user and mileage tracking data"}), 500