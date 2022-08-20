from flask import request

from app import app
from app.init import init_model

handler = init_model()

@app.route('/api/agora_hack', methods=['POST', 'GET'])
def agora_hack():
    result = handler.process(request.json)

    response = {"result": result}

    return response
