from flask import Blueprint, request

from utils.httpResposeUtils import HttpResponseUtils

student_form = Blueprint('student_form', __name__)

@student_form.route('/insert-new-student', methods=['POST'])
def insert_new_student():
    data = request.json
    inserted_data = StudentFormService().insert_new_student(data)
    return HttpResponseUtils.responseForAPIFromArrayData(inserted_data)

