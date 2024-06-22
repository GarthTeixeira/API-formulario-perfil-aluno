from flask import Blueprint, request
from services.escolas_service import EscolaService

from utils.httpResposeUtils import HttpResponseUtils

schools_bp = Blueprint('schools', __name__)

@schools_bp.route('/get-by-area', methods=['GET'])
def get_school_subjects_by_area():
    area_tag = request.args.get('area')
    school_id = request.args.get('school')
    area_data = EscolaService().get_school_subjects_by_area(school_id,area_tag)
    return HttpResponseUtils.responseForAPIFromArrayData(area_data)

@schools_bp.route('/get-all', methods=['GET'])
def get_all():
    all_data = EscolaService().get_all()
    return HttpResponseUtils.responseForAPIFromArrayData(all_data)

@schools_bp.route('/get-schools-names', methods=['GET'])
def get_schools_names():
    all_data = EscolaService().get_schools_names()
    return HttpResponseUtils.responseForAPIFromArrayData(all_data)

@schools_bp.route('/insert-disciplines', methods=['POST'])
def insert_disciplines():
    data = request.json
    inserted_data = EscolaService().insert_list_of_documents(data)
    return HttpResponseUtils.responseForAPIFromArrayData(inserted_data)

@schools_bp.route('/get-school-classes/<school_id>', methods=['GET'])
def get_school_classes(school_id):
    school_classes = EscolaService().get_school_classes(school_id)
    return HttpResponseUtils.responseForAPIFromArrayData(school_classes)