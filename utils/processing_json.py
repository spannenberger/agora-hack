from utils.client import model2client


def preprocess_json(json_file: dict) -> dict:
    input_data = json_file['text']

    if isinstance(input_data, dict):
        input_data = [input_data]

    text_data = []
    products_ids = []

    dict2recognition = {}
    for data in input_data:
        text_data.append(data['name'] + " " +
                         " ".join(data['props']).replace("\t", " "))
        products_ids.append(data['id'])
    dict2recognition.update({'id': products_ids, 'text': text_data})

    return dict2recognition


def postprocess_json(data, result):
    response = [{"id": product_id, "reference_id": model2client(
        model_id)} for product_id, model_id in zip(data['id'], result)]
    return response
