from abc import ABC, abstractmethod
from typing import Dict

import numpy as np
import pandas as pd
import torch
from tqdm import tqdm
from transformers.tokenization_utils_base import BatchEncoding

from app.models import BERTHackModel


class Handler(ABC):
    """Main handler class with all core methods"""

    def process(self, input, **kwargs):
        """Start handler process step by step"""

        preprocessed_input = self.preprocess(input)
        model_output = self.forward_model(preprocessed_input)
        return self.business_logic(model_output, **kwargs)

    @abstractmethod
    def preprocess(self, input):
        """Data preprocessing for the next steps"""

        pass

    @abstractmethod
    def forward_model(self, preprocessed_input):
        """Get model prediction"""

        pass

    @abstractmethod
    def business_logic(self, model_output, **kwargs):
        """Main business logic"""

        pass


class BERTHandler(Handler):
    def __init__(self, model: BERTHackModel, base_file: pd.DataFrame, products_list: Dict) -> None:
        """ Get model & our products

        Args:
            model: GPTHackModel - our model class instance
            base_file: pd.DataFrame - dataframe with ethalon products embeddings
            products_list: Dict - json file with reference_id matched with namings
        """

        self.transformer = model
        self.base_file = base_file
        self.products_list = products_list

    def preprocess(self, text: Dict) -> BatchEncoding:
        """ Preprocess data with tokenizer

        Args:
            text: Dict - text from request 

        Return:
            preprocess_text: BatchEncoding - finaly tokenized data
        """

        preprocess_text = self.transformer.tokenizer(
            text["text"], padding=True, truncation=True, max_length=150, return_tensors='pt')
        return preprocess_text

    def forward_model(self, preprocessed_input: BatchEncoding) -> torch.Tensor:
        """Get model prediction """

        outputs = self.transformer.get_model_prediction(preprocessed_input)
        return outputs

    def business_logic(self, model_outputs: torch.Tensor) -> Dict:
        """ Match model prediction classes with reference_ids 
        from products_list 

        Args:
            model_outputs: torch.Tensor - model predictions

        Return:
            products_matching: Dict - responce dict with matched reference_id & naming
        """

        predicts = []
        for pred in tqdm(model_outputs):
            dists = np.sum((np.square(pred - self.base_file.values.T)), axis=1)
            indices = np.argsort(dists)
            predict_category = self.base_file.columns[indices[0]]
            predicts.append(predict_category)

        return predicts
