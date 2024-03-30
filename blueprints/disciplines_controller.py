from flask import Blueprint, request
from services.disciplines_service import DisciplinesService

from utils.httpResposeUtils import HttpResponseUtils

disciplines_bp = Blueprint('disciplines', __name__)

@disciplines_bp.route('/get-area/<area_tag>', methods=['GET'])
def get_area(area_tag):
    area_data = DisciplinesService().get_by_area(area_tag)
    return HttpResponseUtils.responseForAPIFromArrayData(area_data)

@disciplines_bp.route('/get-all', methods=['GET'])
def get_all():
    all_data = DisciplinesService().get_all()
    return HttpResponseUtils.responseForAPIFromArrayData(all_data)

@disciplines_bp.route('/get-by-school/<school_id>', methods=['GET'])
def get_by_school(school_id):
    all_data = DisciplinesService().get_by_school(school_id)
    return HttpResponseUtils.responseForAPIFromArrayData(all_data)

@disciplines_bp.route('/insert-disciplines', methods=['POST'])
def insert_disciplines():
    data = request.json
    inserted_data = DisciplinesService().insert_list_of_documents(data)
    return HttpResponseUtils.responseForAPIFromArrayData(inserted_data)