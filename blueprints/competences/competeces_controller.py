from flask import Blueprint, request, send_file, abort
from services.competences_services import CompetencesService
from utils.scripts.generate_datasheet_cognitivas import generate_xlsx
import json

from utils.httpResposeUtils import HttpResponseUtils

competences_bp = Blueprint('competences', __name__)

@competences_bp.route('/get-area/<area_tag>', methods=['GET'])
def get_area(area_tag):
    withCompetences = eval(request.args.get('withHabilities').capitalize())
    area_data = CompetencesService().get_by_area(area_tag, withCompetences)
    return HttpResponseUtils.responseForAPIFromArrayData(area_data)

@competences_bp.route('/get-all', methods=['GET'])
def get_all():
    all_data = CompetencesService().get_all()
    return HttpResponseUtils.responseForAPIFromArrayData(all_data)

@competences_bp.route('/get-cognitives-datasheet')
def get_cognitives_datasheet():
    try:

        #area_data = CompetencesService().get_by_area('COGNITIVOS', False)

        f_disciplinas = open('../mock/disciplinas.json')
        disciplinas_info = json.load(f_disciplinas)

        f_competencias = open('../mock/competencias_cognitivas.json')
        competencias_info = json.load(f_competencias)


        generate_xlsx(disciplinas_info, competencias_info)
        # Specify the directory where your files are stored

        
        # Safe join the directory and filename to ensure secure file access
        file_path = "blueprints/competences/data.xlsx"

        
        # Use send_file to send the file directly
        return send_file(file_path, as_attachment=True)
    except FileNotFoundError:
        abort(400)
