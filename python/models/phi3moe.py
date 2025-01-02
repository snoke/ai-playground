import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from typing import List
import os
from huggingface_hub import InferenceClient



class Phi3moe:
    def __init__(self):
        self.client = InferenceClient(api_key="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")
    def prompt(self, messages):

        completion = self.client.chat.completions.create(
            model="microsoft/Phi-3.5-MoE-instruct",
            messages=messages,
            max_tokens=500
        )

        print(completion.choices[0].message)
        return completion.choices[0].message
