from flask import Blueprint, request

from services.formulario_aluno_service import FormularioAlunoService

from utils.httpResposeUtils import HttpResponseUtils

professor_form_bp = Blueprint('professor-form', __name__)


@professor_form_bp.route('health-check', methods=['GET'])
def health_check():
    return HttpResponseUtils.success()

@professor_form_bp.route('/insert-professor', methods=['POST'])
def insert_professor():
    data = request.json
    inserted_data = FormularioAlunoService().insert_professor(data)
    return HttpResponseUtils.reponseFromPostRequest(inserted_data)

@professor_form_bp.route('/insert-resposta', methods=['PUT'])
def insert_resposta():
    data = request.json
    inserted_data = FormularioAlunoService().insert_resposta(data)
    return HttpResponseUtils.responseFromPutRequest(inserted_data)


@professor_form_bp.route('/get-by-school/<school_id>',  methods=['GET'])
def get_by_school(school_id):
    inserted_data = FormularioAlunoService().get_by_school(school_id)
    return HttpResponseUtils.responseForAPIFromArrayData(inserted_data)
