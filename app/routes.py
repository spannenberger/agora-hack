from flask import request

from app import app
from app.init import init_model
from utils.processing_json import preprocess_json, postprocess_json
import json

handler = init_model()

@app.route('/match_products', methods=['POST', 'GET'])
def agora_hack():
    data = preprocess_json(request.json)

    result = handler.process(data)

    response = postprocess_json(data, result)

    return json.dumps(response)
