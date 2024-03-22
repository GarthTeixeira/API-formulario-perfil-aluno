from flask import Blueprint, request
from services.competences_services import CompetencesService

from utils.httpResposeUtils import HttpResponseUtils

competences_bp = Blueprint('competences', __name__)

@competences_bp.route('/get-area/<area_tag>', methods=['GET'])
def get_area(area_tag):
    withCompetences = eval(request.args.get('withHabilities').capitalize())
    area_data = CompetencesService().get_area(area_tag, withCompetences)
    return HttpResponseUtils.responseForAPIFromArrayData(area_data)
