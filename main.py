from flask import Flask, request, jsonify
from blueprints.competences.competeces_controller import competences_bp


app = Flask(__name__)
app.register_blueprint(competences_bp, url_prefix='/competences')


if __name__ == '__main__':
    app.run(debug=True)