from flask import Flask, request, jsonify
from blueprints.competences.competeces_controller import competences_bp
from blueprints.disciplines_controller import disciplines_bp
from blueprints.formulario_aluno_controller import student_form_bp
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
app.register_blueprint(competences_bp, url_prefix='/competences')
app.register_blueprint(disciplines_bp, url_prefix='/disciplines')
app.register_blueprint(student_form_bp, url_prefix='/student_form')


if __name__ == '__main__':
    app.run(debug=True)