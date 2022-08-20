from utils.client import model2client


def preprocess_json(json_file: dict) -> dict:

    if isinstance(json_file, dict):
        json_file = [json_file]

    text_data = []
    products_ids = []

    dict2recognition = {}
    for data in json_file:
        text_data.append(data['name'] + " " +
                         " ".join(data['props']).replace("\t", " "))
        products_ids.append(data['id'])
    dict2recognition.update({'id': products_ids, 'text': text_data})

    return dict2recognition


def postprocess_json(data, result):
    response = [{"id": product_id, "reference_id": model2client(
        model_id)} for product_id, model_id in zip(data['id'], result)]
    return response
