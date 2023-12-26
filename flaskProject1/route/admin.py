import pymysql
from flask import Blueprint, jsonify, g
from . import database


admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/rowadmin', methods=['GET'])
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


@admin_bp.route('/editor/customer/<email>', methods=['DELETE'])
def delete_customer(email):
    try:
        with pymysql.connect(**database.connectionString) as con:
            cursor = con.cursor()

            # 스키마 변경
            cursor.execute("USE editor;")

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