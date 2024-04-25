from flask import Blueprint, request

from services.formulario_aluno_service import FormularioAlunoService

from utils.httpResposeUtils import HttpResponseUtils

student_form_bp = Blueprint('student_form', __name__)

@student_form_bp.route('/insert-form', methods=['POST'])
def insert_form():
    data = request.json
    inserted_data = FormularioAlunoService().insert_formulario(data)
    return HttpResponseUtils.responseForAPIFromMessage(inserted_data)

@student_form_bp.route('/get-by-student', methods=['POST'])
def get_by_student():
    data = request.json
    inserted_data = FormularioAlunoService().get_by_aluno(data)
    return HttpResponseUtils.responseForAPIFromArrayData(inserted_data)

