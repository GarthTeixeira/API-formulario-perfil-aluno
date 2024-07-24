from flask import Blueprint, request

from services.formulario_aluno_service import FormularioAlunoService

from utils.httpResposeUtils import HttpResponseUtils

student_form_bp = Blueprint('student_form', __name__)

@student_form_bp.route('/insert-form', methods=['POST'])
def insert_form():
    data = request.json
    inserted_data = FormularioAlunoService().insert_formulario(data)
    return HttpResponseUtils.reponseFromPostRequest(inserted_data)

@student_form_bp.route('/insert-professor', methods=['POST'])
def insert_professor():
    data = request.json
    inserted_data = FormularioAlunoService().insert_professor(data)
    return HttpResponseUtils.reponseFromPostRequest(inserted_data)

@student_form_bp.route('/insert-resposta', methods=['PUT'])
def insert_grafo():
    data = request.json
    inserted_data = FormularioAlunoService().insert_grafo(data)
    return HttpResponseUtils.responseFromPutRequest(inserted_data)

@student_form_bp.route('/get-by-student', methods=['POST'])
def get_by_student():
    data = request.json
    inserted_data = FormularioAlunoService().get_by_aluno(data)
    return HttpResponseUtils.responseForAPIFromArrayData(inserted_data)

