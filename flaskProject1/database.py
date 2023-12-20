import pymysql
from flask import jsonify

connectionString = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'passwd',
    'charset': 'utf8',
    'cursorclass': pymysql.cursors.DictCursor
}

def getItems(sort, keyword, schema1, schema2):
    try:
        # 데이터베이스 연결 시도
        with pymysql.connect(database=schema1, **connectionString) as con1, \
             pymysql.connect(database=schema2, **connectionString) as con2:

            cursor1 = con1.cursor()
            cursor2 = con2.cursor()

            sql = f"SELECT * FROM items WHERE name LIKE %s ORDER BY {sort};"
            cursor1.execute(sql, [f"%{keyword}%"])
            result1 = cursor1.fetchall()

            cursor2.execute(sql, [f"%{keyword}%"])
            result2 = cursor2.fetchall()

            # 두 스키마의 결과를 합쳐서 반환
            return jsonify({'items': result1 + result2})

    except pymysql.Error as e:
        print(f"Error fetching items: {e}")
        return jsonify({"message": "Error fetching items"}), 500

def get_customer_data(schema1, schema2):
    try:
        with pymysql.connect(database=schema1, **connectionString) as con1, \
             pymysql.connect(database=schema2, **connectionString) as con2:

            cursor1 = con1.cursor()
            cursor2 = con2.cursor()

            sql = "SELECT * FROM customer;"
            cursor1.execute(sql)
            result1 = cursor1.fetchall()

            cursor2.execute(sql)
            result2 = cursor2.fetchall()

            # 두 스키마의 결과를 합쳐서 반환
            return jsonify({'users': result1 + result2})

    except Exception as e:
        print(e)
        return jsonify({"message": "Error fetching customer data"}), 500

def idCheck(user_id, pwd, schema1, schema2):
    try:
        with pymysql.connect(database=schema1, **connectionString) as con:
            cursor = con.cursor()
            # 여기서 스키마를 선택할 수 있도록 변경
            sql = f"SELECT * FROM {schema1}.user WHERE email = %s AND password = %s UNION SELECT * FROM {schema2}.user WHERE email = %s AND password = %s;"
            cursor.execute(sql, [user_id, pwd, user_id, pwd])
            result = cursor.fetchall()
            return result
    except Exception as e:
        print(e)


# database.py

def addUserInfo(userId, userPwd, schema):
    try:
        with pymysql.connect(database=schema, **connectionString) as con:
            cursor = con.cursor()
            sql = f"""INSERT INTO user (email, password) VALUES("{userId}","{userPwd}")"""
            cursor.execute(sql)
            con.commit()

        # 변경된 부분: 반환값을 3개로 변경하고 성공 메시지를 반환
        return jsonify({"message": "User added successfully", "status": "success"}), 200, {'Content-Type': 'application/json'}

    except Exception as e:
        print(e)
        # 변경된 부분: 실패 시 에러 메시지와 상태를 반환
        return jsonify({"message": "Error adding user", "status": "error"}), 500, {'Content-Type': 'application/json'}

