from flask import Blueprint,request, Response, stream_with_context
import requests

question_bp = Blueprint('question',__name__)

@question_bp.route('generate',methods=['POST'])
def generate():
    model_name = 'llama3.2'
    prompt = request.json['question']
    data = {'model': model_name, 'prompt': prompt}
    response = requests.post('http://localhost:11434/api/generate', json=data, stream=True)
    print('response',response.headers.get('Content-Type') )
    return Response(stream_with_context(response.iter_lines()), mimetype='application/x-ndjson')