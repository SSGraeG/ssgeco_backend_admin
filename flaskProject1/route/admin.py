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