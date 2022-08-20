import json

import torch
from torch import nn

from transformers import GPT2ForSequenceClassification, GPT2Tokenizer, DistilBertTokenizer, DistilBertModel
from transformers.tokenization_utils_base import BatchEncoding
import pandas as pd

from app.arcface import ArcMarginProduct

class BertModel(nn.Module):
    def __init__(self, 
                 bert_model, 
                 num_classes=472, 
                 last_hidden_size=768):
        
        super().__init__()
        self.bert_model = bert_model
        self.arc_margin = ArcMarginProduct(last_hidden_size, 
                                           num_classes,
                                           s=30.0, 
                                           m=0.50, 
                                           easy_margin=False)
    
    def get_bert_features(self, batch):
        output = self.bert_model(input_ids=batch['input_ids'], attention_mask=batch['attention_mask'])
        last_hidden_state = output.last_hidden_state # shape: (batch_size, seq_length, bert_hidden_dim)
        CLS_token_state = last_hidden_state[:, 0, :] # obtaining CLS token state which is the first token.
        return CLS_token_state
    
    # def forward(self, batch):
    #     CLS_hidden_state = self.get_bert_features(batch)
    #     output = self.arc_margin(CLS_hidden_state, batch['label'])
    #     return output


class GPTHackModel:

    def __init__(self, model_path: str, base_file_path: str) -> None:
        """ Initialize model, tokenizer & base file

        Args:
            model_path: str - local folder path with model's files
            base_file_path: str - json file with model's classes [0, 1, ..., 471, 472] matched with reference_id
        """

        self.tokenizer = GPT2Tokenizer.from_pretrained(
            "sberbank-ai/rugpt3medium_based_on_gpt2")
        self.tokenizer.add_special_tokens({'pad_token': '<pad>'})

        self.model = GPT2ForSequenceClassification.from_pretrained(model_path)

        self.device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
        self.model.to(self.device)

        with open(base_file_path, "r") as file:
            self.base_file = json.load(file)

    def get_model_prediction(self, preprocessed_text: BatchEncoding) -> torch.Tensor:
        """ Batch data model prediction
        Args:
            preprocessed_text: BatchEncoding - tokenized batch of data
        Return:
            model_outputs: torch.Tensor - model logits prediction with shape [batch_size, labels_num]
        """
        
        self.model.eval()
        with torch.no_grad():
            model_outputs = self.model(**preprocessed_text).logits
        # breakpoint()
        return model_outputs



class BERTHackModel:

    def __init__(self, model_path: str, product_matches_path: str) -> None:
        """ Initialize model, tokenizer & base file

        Args:
            model_path: str - local folder path with model's files
            base_file_path: str - json file with model's classes [0, 1, ..., 471, 472] matched with reference_id
        """

        self.tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased")

        self.model = BertModel(DistilBertModel.from_pretrained('distilbert-base-uncased'))
        self.model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))

        self.device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
        self.model.to(self.device)

        # with open(product_matches_path, "r") as file:
        #     self.product_matches_path = json.load(file)

    def get_model_prediction(self, preprocessed_text: BatchEncoding) -> torch.Tensor:
        """ Batch data model prediction
        Args:
            preprocessed_text: BatchEncoding - tokenized batch of data
        Return:
            model_outputs: torch.Tensor - model logits prediction with shape [batch_size, labels_num]
        """
        
        self.model.eval()
        with torch.no_grad():
            model_outputs = self.model.get_bert_features(preprocessed_text).detach().cpu().numpy()
        # breakpoint()
        return model_outputs


