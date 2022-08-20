from abc import ABC, abstractmethod
from typing import Dict

import torch
from transformers.tokenization_utils_base import BatchEncoding
from torch import nn

import pandas as pd
from app.models import GPTHackModel
import numpy as np


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


class NLPHandler(Handler):
    def __init__(self, model: GPTHackModel, products_list: Dict) -> None:
        """ Get model & our products

        Args:
            model: GPTHackModel - our model class instance
            products_list: Dict - json file with reference_id matched with namings
        """

        self.transformer = model
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

        products_matching = {
            # "naming": [],
            "id": [],
        }
        m = nn.Softmax(dim=1)
        pred_class_ids = torch.argmax(model_outputs, axis=-1).tolist()
        # preds = m(model_outputs)  # 0.0273, 0.0237, 0.0225, 0.0164, 0.0119
        # top_5 = torch.topk(preds.flatten(), 5)
        # breakpoint()
        # full_preds = torch.topk(model_outputs.flatten(), 5)  # [2.5247, 2.3818, 2.3293, 2.0163, 1.6890]
        ans = self.transformer.model.config.id2label[pred_class_ids[0]]
        pred_classes = [self.transformer.base_file[str(
            label)] for label in pred_class_ids]

        for item in pred_classes:
            # products_matching["naming"].append(self.products_list[item])
            products_matching["id"].append(item)

        return products_matching


class BERTHandler(Handler):
    def __init__(self, model, base_file: pd.DataFrame, products_list: Dict) -> None:
        """ Get model & our products

        Args:
            model: GPTHackModel - our model class instance
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

        preprocess_text = self.transformer.tokenizer(text["text"], padding=True, truncation=True, max_length=150, return_tensors='pt')
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

        dists = np.sum((np.square(model_outputs - self.base_file.values.T)), axis=1)
        indices = np.argsort(dists)
        predict_category = self.base_file.columns[indices[0]]

        return predict_category
