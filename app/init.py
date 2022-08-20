import os
import random

import numpy as np
import pandas as pd
import torch

from app.business_logic import BERTHandler, GPTHandler
from app.models import BERTHackModel, GPTHackModel

torch.manual_seed(0)
random.seed(0)
np.random.seed(0)


def init_model():
    model_path = os.getenv("MODEL_PATH", "")  # get trained model folder path
    base_file_path = os.getenv("BASE_FILE", "")  # get dict with model classes & reference_id
    product_matches_path = os.getenv("PRODUCTS_MATCHES_PATH", "")

    base_file = pd.read_csv(base_file_path)
    
    model = BERTHackModel(model_path, product_matches_path)
    nlp_handler = BERTHandler(model, base_file, product_matches_path)

    return nlp_handler
