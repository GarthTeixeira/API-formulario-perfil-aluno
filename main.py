from flask import Flask, request, jsonify
from blueprints.competeces_controller import competences_bp
from blueprints.disciplines_controller import disciplines_bp
from blueprints.formulario_aluno_controller import professor_form_bp
from blueprints.escolas_controller import schools_bp
from blueprints.question_controller import question_bp
from flask_cors import CORS

#FIX-ME: fazer tratamento de exceptions
#TODO: padronizar definição de nomes portugues-ingles
#TODO: adicionar parâmetros mudança de ambiente


app = Flask(__name__)
CORS(app)
app.register_blueprint(competences_bp, url_prefix='/competences')
app.register_blueprint(disciplines_bp, url_prefix='/disciplinas')
app.register_blueprint(professor_form_bp, url_prefix='/professor-form')
app.register_blueprint(schools_bp, url_prefix='/schools')
app.register_blueprint(question_bp, url_prefix = '/question')

if __name__ == '__main__':
    app.run(debug=True)