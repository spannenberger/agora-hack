import json

from flask import request
from utils.processing_json import postprocess_json, preprocess_json

from app import app
from app.init import init_model

handler = init_model()

@app.route('/match_products', methods=['POST', 'GET'])
def agora_hack():
    data = preprocess_json(request.json)

    result = handler.process(data)

    response = postprocess_json(data, result)

    return json.dumps(response)
