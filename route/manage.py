import pymysql
from flask import Blueprint, request, jsonify, g
from . import database

manage_bp = Blueprint('manage', __name__)

@manage_bp.route('/company/user', methods=['GET'])
def get_user_info_and_company_id_and_role():
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

@manage_bp.route('/company/user/<email>', methods=['DELETE'])
def delete_user(email):
    try:
        with pymysql.connect(**database.connectionString) as con:
            cursor = con.cursor()
            user_schema = f"company_{g.company_id}"
            cursor.execute(f"USE {user_schema};")
            sql = "DELETE FROM user WHERE email = %s;"
            cursor.execute(sql, (email,))
            con.commit()
            return jsonify({"message": f"User {email} deleted successfully"}), 200
    except Exception as e:
        print("Error deleting user:", e)
        return jsonify({"message": "Error deleting user"}), 500

@manage_bp.route('/company/user/coupon/<coupon_id>', methods=['DELETE'])
def delete_coupon(coupon_id):
    try:
        with pymysql.connect(**database.connectionString) as con:
            cursor = con.cursor()
            user_schema = f"company_{g.company_id}"
            cursor.execute(f"USE {user_schema};")

            # 관련 레코드를 mileage_tracking 테이블에서 삭제
            sql_delete_tracking = "DELETE FROM mileage_tracking WHERE mileage_category_id = %s;"
            cursor.execute(sql_delete_tracking, (coupon_id,))

            # 쿠폰 삭제
            sql_delete_coupon = "DELETE FROM mileage_category WHERE id = %s;"
            cursor.execute(sql_delete_coupon, (coupon_id,))

            con.commit()
            return jsonify({"message": f"Coupon {coupon_id} deleted successfully"}), 200
    except Exception as e:
        print("Error deleting coupon:", e)
        return jsonify({"message": "Error deleting coupon"}), 500

@manage_bp.route('/api/getCompanyName/<company_id>', methods=['GET'])
def get_company_name(company_id):
    try:
        with pymysql.connect(**database.connectionString) as con:
            cursor = con.cursor()
            sql = "SELECT company_name FROM customer WHERE company_id = %s;"
            cursor.execute(sql, [company_id])
            result = cursor.fetchone()

            if result:
                company_name = result['company_name']
                return jsonify({'company_name': company_name})
            else:
                return jsonify({"message": "Company name not found"}), 404

    except Exception as e:
        print(f"Error in get_company_name: {e}")
        return jsonify({"message": "Error fetching company name"}), 500


@manage_bp.route('/company/user/coupon', methods=['GET', 'POST'])
def manage_coupons():
    if request.method == 'GET':
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

                # 쿠폰 정보 조회 쿼리
                sql = "SELECT * FROM mileage_category;"
                cursor.execute(sql)
                coupon_data = cursor.fetchall()

                return jsonify({'coupons': coupon_data})

        except Exception as e:
            print("Error fetching coupon data:", e)
            return jsonify({"message": "Error fetching coupon data"}), 500
    elif request.method == 'POST':
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

                # POST 요청에서 쿠폰 정보 가져오기
                data = request.json
                coupon_name = data.get('name')
                usepoint = data.get('usepoint')
                category = data.get('category')  # Added line to get category

                # 쿠폰을 coupon 테이블에 추가
                sql = "INSERT INTO mileage_category (name, usepoint, category) VALUES (%s, %s, %s);"
                cursor.execute(sql, (coupon_name, usepoint, category))
                con.commit()

                # 생성한 쿠폰 정보 응답
                created_coupon_id = cursor.lastrowid
                created_coupon = {
                    'id': created_coupon_id,
                    'name': coupon_name,
                    'usepoint': usepoint,
                    'category': category  # Include category in the response
                }

                return jsonify({'coupon': created_coupon}), 201

        except Exception as e:
            print("Error creating coupon:", e)
            return jsonify({"message": "Error creating coupon"}), 500

@manage_bp.route('/company/user/mileage', methods=['GET'])
def get_mileage_data():
    try:
        # 클라이언트에서 보낸 Company-ID와 페이지 정보를 헤더에서 읽어옴
        company_id = request.headers.get('Company-ID')
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 10))

        # Company-ID가 None이면 디폴트 값으로 설정
        if company_id is None:
            company_id = 'default_company_id'

        with pymysql.connect(**database.connectionString) as con:
            cursor = con.cursor()

            # 현재 사용자의 스키마로 전환
            user_schema = f"company_{company_id}"
            cursor.execute(f"USE {user_schema};")

            # 마일리지 정보 조회 쿼리 (페이징 처리)
            offset = (page - 1) * page_size
            sql = f"SELECT * FROM mileage_tracking LIMIT {offset}, {page_size};"
            cursor.execute(sql)
            mileage_data = cursor.fetchall()

            return jsonify({"mileage_tracking": mileage_data})

    except Exception as e:
        print("Error fetching mileage data:", e)
        return jsonify({"message": "Error fetching mileage data"}), 500