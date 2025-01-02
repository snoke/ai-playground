from transformers import MarianMTModel, MarianTokenizer
class OpusMulEn:
    def __init__(self):
        self.tokenizer = MarianTokenizer.from_pretrained("Helsinki-NLP/opus-mt-mul-en")
        self.model = MarianMTModel.from_pretrained("Helsinki-NLP/opus-mt-mul-en")
    def translate(self,text, fromLang):
        inputs_tgt = self.tokenizer('>>' + fromLang + '<< ' + text, return_tensors="pt", padding=True, truncation=True)
        final_tokens = self.model.generate(**inputs_tgt)
        translated_text = self.tokenizer.decode(final_tokens[0], skip_special_tokens=True)
        return translated_text