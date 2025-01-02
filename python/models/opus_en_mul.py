from transformers import MarianMTModel, MarianTokenizer
class OpusEnMul:
    def __init__(self):
        self.tokenizer = MarianTokenizer.from_pretrained("Helsinki-NLP/opus-mt-en-mul")
        self.model = MarianMTModel.from_pretrained("Helsinki-NLP/opus-mt-en-mul")
    def translate(self,text, toLang):
        inputs_tgt = self.tokenizer('>>' + toLang + '<< ' + text, return_tensors="pt", padding=True, truncation=True)
        final_tokens = self.model.generate(**inputs_tgt)
        translated_text = self.tokenizer.decode(final_tokens[0], skip_special_tokens=True)
        return translated_text