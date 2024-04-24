from flask import Blueprint, request

from services.formulario_aluno_service import FormularioAlunoService

from utils.httpResposeUtils import HttpResponseUtils

student_form_bp = Blueprint('student_form', __name__)

@student_form_bp.route('/insert-new-student', methods=['POST'])
def insert_new_student():
    data = request.json
    inserted_data = FormularioAlunoService().insert_new_student(data)
    return HttpResponseUtils.responseForAPIFromArrayData(inserted_data)

@student_form_bp.route('/get-by-student', methods=['POST'])
def get_by_student():
    data = request.json
    inserted_data = FormularioAlunoService().get_by_aluno_data(data)
    return HttpResponseUtils.responseForAPIFromArrayData(inserted_data)

