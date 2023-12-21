#database.py
import pymysql
from flask import jsonify
from pymysql import connect

# from datetime import datetime


connectionString = {
    'host': '127.0.0.1',
    'port': 3306,
    'database': 'editor',
    'user': 'root',
    'password': 'passwd',
    'charset': 'utf8',
    'cursorclass': pymysql.cursors.DictCursor
}

try:
    # 데이터베이스 연결 시도
    with connect(**connectionString) as con:
        print("Database connected successfully!")
        # 여기서 데이터베이스 작업 수행
except pymysql.Error as e:
    # 데이터베이스 연결 중 오류가 발생한 경우
    print(f"Error connecting to the database: {e}")


def get_customer_data():
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()
            sql = "SELECT * FROM customer;"
            cursor.execute(sql)
            customer_data = cursor.fetchall()
            return jsonify({'users': customer_data})

    except Exception as e:
        print(e)
        return jsonify({"message": "Error fetching customer data"}), 500
def idCheck(user_id, pwd):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()
            sql = "SELECT * FROM customer " + "where email = %s and password = %s;"
            cursor.execute(sql, [user_id, pwd])
            result = cursor.fetchall()
            return result
    except Exception as e:
        print(e)


def addUserInfo(userId, userPwd):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()
            sql = f"""INSERT INTO customer (email, password) VALUES("{userId}","{userPwd}")"""
            print(cursor.execute(sql))
            userInfo = cursor.fetchall()
            con.commit()

        return userInfo, 200, {'Content-Type': 'application/json'}

    except Exception as e:
        print(e)