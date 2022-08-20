import json
import os
import random

import numpy as np
import torch
import pandas as pd

from app.business_logic import NLPHandler, BERTHandler
from app.models import GPTHackModel, BERTHackModel

torch.manual_seed(0)
random.seed(0)
np.random.seed(0)


def init_model():
    model_path = os.getenv("MODEL_PATH", "")  # get trained model folder path
    base_file_path = os.getenv("BASE_FILE", "")  # get dict with model classes & reference_id
    product_matches_path = os.getenv("PRODUCTS_MATCHES_PATH", "")
    # products_list_path = os.getenv("PRODUCTS_LIST", "")  # get dict with reference_id & naming

    # with open(products_list_path, "r") as file:
    #     products_list = json.load(file)

    base_file = pd.read_csv(base_file_path)
    
    # model = GPTHackModel(model_path, base_file_path)
    model = BERTHackModel(model_path, product_matches_path)
    nlp_handler = BERTHandler(model, base_file, product_matches_path)

    return nlp_handler
