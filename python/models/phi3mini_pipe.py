from transformers import pipeline


class Phi3mini:
    def __init__(self, model_name: str = "/root/.cache/huggingface/hub/models--microsoft--Phi-3.5-mini-instruct/snapshots/af0dfb8029e8a74545d0736d30cb6b58d2f0f3f0"):
        self.model_name = model_name
        print('loaded')
    def prompt(self, messages):
        print('text-generation')
        pipe = pipeline("text-generation", model=self.model_name, trust_remote_code=True)
        print('text-generation2')
        response = pipe(messages)
        print('text-generation3')
        print(response)
        return response