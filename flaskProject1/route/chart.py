from flask import Blueprint, jsonify
from . import database

chart_bp = Blueprint('chart', __name__)


@chart_bp.route('/api/get_data', methods=['GET'])
def get_customer_data():
    # database 모듈에서 get_customer_data 함수를 호출하여 전체 사용자 데이터를 가져옵니다.
    return database.get_customer_data()

