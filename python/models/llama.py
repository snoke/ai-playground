import requests
import torch
from PIL import Image
from transformers import MllamaForConditionalGeneration, AutoProcessor

class Llama:
    def __init__(self):
        model_id = "meta-llama/Llama-3.2-11B-Vision-Instruct"

        self.model = MllamaForConditionalGeneration.from_pretrained(
            model_id,
            torch_dtype=torch.bfloat16,
            device_map="auto",
        )
        self.processor = AutoProcessor.from_pretrained(model_id)

    def prompt(image, text):
        image = Image.open(requests.get(image, stream=True).raw)

        messages = [
            {"role": "user", "content": [
                {"type": "image"},
                {"type": "text", "text": text}
            ]}
        ]
        input_text = self.processor.apply_chat_template(messages, add_generation_prompt=True)
        inputs = self.processor(
            image,
            input_text,
            add_special_tokens=False,
            return_tensors="pt"
        ).to(self.model.device)

        output = self.model.generate(**inputs, max_new_tokens=30)
        print(self.processor.decode(output[0]))
        return output[0]