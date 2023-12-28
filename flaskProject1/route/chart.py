from flask import Blueprint, jsonify
from . import database

chart_bp = Blueprint('chart', __name__)


@chart_bp.route('/api/get_data', methods=['GET'])
def get_customer_data():
    # database 모듈에서 get_customer_data 함수를 호출하여 전체 사용자 데이터를 가져옵니다.
    return database.get_customer_data()


@chart_bp.route('/api/getChartData/<usernum>', methods=['GET'])
def get_chart_data(usernum):
    # 여기에서 usernum을 기반으로 차트 데이터를 가져와서 응답합니다.
    # 데이터베이스 조회 등을 수행하여 실제 차트 데이터를 가져오는 로직이 들어가야 합니다.

    # 예시로 임의의 데이터를 반환합니다. 실제로는 데이터베이스에서 조회해야 합니다.
    chart_data = {'usernum': usernum, 'chart': 'data'}

    return jsonify(chart_data)