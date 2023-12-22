from datetime import datetime, timedelta
import pymysql
from flask import jsonify
from pymysql import connect

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

# ... (이전 코드)

def addUserInfo(userId, userPwd, name, phone, start_date, industryCategory, isSubscribed):
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
                INSERT INTO customer (email, password, company_name, phone, start_date, category, subscription_status, end_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (userId, userPwd, name, phone, start_date, industryCategory, subscription_status, expiration_date))
            con.commit()

            # 회원가입 성공 후에 새로운 스키마 생성 및 테이블 생성
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

                # 테이블 생성 쿼리
                create_tables_query = """
                                    CREATE TABLE IF NOT EXISTS `user` (
                                        `email` VARCHAR(45) NOT NULL,
                                        `name` VARCHAR(45) NOT NULL,
                                        `phone` VARCHAR(45) NULL DEFAULT NULL,
                                        `address` VARCHAR(50) NULL DEFAULT NULL,
                                        `mileage` INT NULL DEFAULT '0',
                                        `password` VARCHAR(45) NOT NULL,
                                        PRIMARY KEY (`email`)
                                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

                                    CREATE TABLE IF NOT EXISTS `mileage` (
                                        `id` INT NOT NULL AUTO_INCREMENT,
                                        `name` VARCHAR(45) NULL,
                                        `usepoint` INT NULL,
                                        PRIMARY KEY (`id`)
                                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

                                    CREATE TABLE IF NOT EXISTS `mileage_tracking` (
                                        `id` INT NOT NULL AUTO_INCREMENT,
                                        `use_date` DATETIME NULL DEFAULT NULL,
                                        `user_email` VARCHAR(45) NOT NULL,
                                        `mileage_id` INT NOT NULL,
                                        PRIMARY KEY (`id`),
                                        INDEX `fk_tracking_user_idx` (`user_email` ASC) VISIBLE,
                                        INDEX `fk_mileage_tracking_mileage1_idx` (`mileage_id` ASC) VISIBLE,
                                        CONSTRAINT `fk_tracking_user`
                                            FOREIGN KEY (`user_email`)
                                            REFERENCES `user` (`email`)
                                            ON DELETE CASCADE
                                            ON UPDATE CASCADE,
                                        CONSTRAINT `fk_mileage_tracking_mileage1`
                                            FOREIGN KEY (`mileage_id`)
                                            REFERENCES `mileage` (`id`)
                                            ON DELETE CASCADE
                                            ON UPDATE CASCADE
                                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

                                    CREATE TABLE IF NOT EXISTS `coupon` (
                                        `id` INT NOT NULL AUTO_INCREMENT,
                                        `name` VARCHAR(100) NOT NULL,
                                        `usepoint` INT NOT NULL,
                                        PRIMARY KEY (`id`)
                                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

                                    CREATE TABLE IF NOT EXISTS `coupon_tracking` (
                                        `id` INT NOT NULL AUTO_INCREMENT,
                                        `use_date` DATETIME NOT NULL,
                                        `user_email` VARCHAR(45) NOT NULL,
                                        `coupon_id` INT NOT NULL,
                                        PRIMARY KEY (`id`),
                                        INDEX `fk_coupon_tracking_user1_idx` (`user_email` ASC) VISIBLE,
                                        INDEX `fk_coupon_tracking_coupon1_idx` (`coupon_id` ASC) VISIBLE,
                                        CONSTRAINT `fk_coupon_tracking_user1`
                                            FOREIGN KEY (`user_email`)
                                            REFERENCES `user` (`email`)
                                            ON DELETE CASCADE
                                            ON UPDATE CASCADE,
                                        CONSTRAINT `fk_coupon_tracking_coupon1`
                                            FOREIGN KEY (`coupon_id`)
                                            REFERENCES `coupon` (`id`)
                                            ON DELETE CASCADE
                                            ON UPDATE CASCADE
                                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
                                """

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

def get_user_info_and_company_id(user_id, pwd):
    try:
        with connect(**connectionString) as con:
            cursor = con.cursor()
            sql = "SELECT email, company_id FROM customer WHERE email = %s AND password = %s;"
            cursor.execute(sql, [user_id, pwd])
            result = cursor.fetchone()

            if result:
                user_info = {'email': result['email']}
                company_id = result['company_id']
                return user_info, company_id

            return None, None

    except Exception as e:
        print(e)
        return None, None


