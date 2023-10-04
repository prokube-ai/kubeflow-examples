from transformers import AutoTokenizer
import transformers
import torch
import os
import json
from loguru import logger
from huggingface_hub import login
from typing import Dict, Union
from kserve import (
    Model,
    InferRequest,
    InferResponse,
)

import os
import json
import transformers
from typing import Union, Dict
from kserve import Model, InferRequest, InferResponse
from transformers import AutoTokenizer


class Llama2ChatPredictor(Model):
    def __init__(
        self,
        name: str,
        hf_model_string: str = "meta-llama/Llama-2-7b-chat-hf",
        loguru_loglevel: str = "INFO",
        device: Union[int, str] = "auto",
    ):
        """
        Initialize the Llama2ChatPredictor.

        Parameters:
            name: The name of the model.
            hf_model_string: The identifier of the Hugging Face model.
            loguru_loglevel: Logging level for loguru.
            device: The device to run the model on (0, 1, ..., 'cpu', 'gpu').
        """
        super().__init__(name=name)
        os.environ["LOGURU_LEVEL"] = loguru_loglevel
        self.device = device
        self.hf_model_string = hf_model_string
        self.load()
        self.ready = True

    def load(self):
        """
        Load the model weights and tokenizer from Hugging Face and create the pipeline.
        """
        login(token=os.environ["HF_ACCESS_TOKEN"])
        logger.info(f"Loading weights and tokenizer for model: {self.hf_model_string}")
        self.tokenizer = AutoTokenizer.from_pretrained(self.hf_model_string)
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.pipeline = transformers.pipeline(
            "text-generation",
            model=self.hf_model_string,
            torch_dtype=torch.float32
            if not torch.cuda.is_available()
            else torch.float16,
            device=self.device,
        )


    def preprocess(
        self,
        payload: Union[bytes, InferRequest],
        headers: Dict[str, str] = None,  
    ) -> Dict:
        """
        Preprocess the payload into the format expected by the predict method.

        Parameters:
            payload: The input payload, as a bytes string or InferRequest.
            headers: Additional headers (unused here, but expected in base class).

        Returns:
            the payload as a dict
        """
        return payload if type(payload) == dict else json.loads(payload)


    def predict(
        self,
        payload: Dict,
        headers: Dict[str, str] = None,
    ) -> Union[str, InferResponse]:
        """
        Generate predictions using the input payload.

        Parameters:
            payload: The input payload, preprocessed to dict format.
            headers: Additional headers (unused here, but expected in base class).

        Returns:
            A string containing the generated text.
        """
        sequences = self.pipeline(
            f"{payload['instances']}\n",
            do_sample=True,
            top_k=payload["top_k"],
            num_return_sequences=1,
            eos_token_id=self.tokenizer.eos_token_id,
            max_length=payload["max_length"],
        )
        return sequences[0]["generated_text"]
