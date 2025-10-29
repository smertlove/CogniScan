import numpy as np
import torch
from transformers import AutoTokenizer, AutoModel

import logging


class Encoder:

    def __init__(self, model_name="alexyalunin/RuBioRoBERTa"):
        self.logger = logging.Logger("Encoder")
        self.logger.setLevel(logging.INFO)

        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.logger.info("Tokenizer loaded")

        self.model = AutoModel.from_pretrained(model_name)
        self.logger.info("Encoder model loaded")

        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.logger.info(f'Device set to use "{self.device}"')
        self.model.eval()

    def encode(self, texts, batch_size=32):
        """Convert list of texts to embeddings"""
        all_embeddings = []

        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i : i + batch_size]

            inputs = self.tokenizer(
                batch_texts,
                padding=True,
                truncation=True,
                max_length=512,
                return_tensors="pt",
            ).to(self.device)

            # Get embeddings
            with torch.no_grad():
                outputs = self.model(**inputs)
                embeddings = self.mean_pooling(
                    outputs.last_hidden_state, inputs["attention_mask"]
                )
                embeddings = embeddings.cpu().numpy()

            all_embeddings.append(embeddings)

        return np.vstack(all_embeddings)

    def mean_pooling(self, model_output, attention_mask):
        """
        Усредняет эмбединги токенов с респектом к падингу,
        таким образом получает эмбединг предложения.
        """
        # Привели маску к размерности эмбедингов токенов
        attention_mask_expanded = (
            attention_mask.unsqueeze(-1).expand(model_output.size()).float()
        )
        # Усредняет эмбединги токенов с респектом к падингу
        return torch.sum(model_output * attention_mask_expanded, 1) / torch.clamp(
            attention_mask_expanded.sum(1), min=1e-9
        )
