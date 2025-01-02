import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from typing import List
import os
from transformers import logging
logging.set_verbosity_debug()
from transformers import AutoConfig
class Phi3mini:
    def __init__(self, model_name: str = "microsoft/Phi-3.5-mini-instruct"):
        # Modell und Tokenizer herunterladen
        print('init token')
        # Tokenizer laden
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

        print('init model')
        # Modell laden
        self.model = AutoModelForCausalLM.from_pretrained(model_name)
        print('init done')

    def prompt(self, prompt_text: str, max_length: int = 500) -> str:
        # Eingabe tokenisieren
        inputs = self.tokenizer(prompt_text, return_tensors="pt")

        # Modell ausführen
        outputs = self.model.generate(
            inputs.input_ids,
            max_length=max_length,
            num_return_sequences=1,
            do_sample=True,
            temperature=0.7
        )

        # Ausgabe decodieren
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response