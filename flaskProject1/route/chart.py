from flask import Blueprint, request, jsonify
from . import database

chart_bp = Blueprint('chart', __name__)

@chart_bp.route('/api/get_data', methods=['GET'])
def get_customer_data():
    return database.get_customer_data()


@chart_bp.route('/api/getChartData/<usernum>', methods=['GET'])
def get_chart_data(usernum):
    # 여기에서 usernum을 기반으로 차트 데이터를 가져와서 응답합니다.
    # 사용자 번호에 따른 차트 데이터를 반환하도록 데이터베이스 조회 등을 수행합니다.
    # 예시: chart_data = get_chart_data_from_database(usernum)
    chart_data = {'usernum': usernum, 'chart': 'data'}
    return jsonify(chart_data)