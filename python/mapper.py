import json
from collections import defaultdict

# Sprachsets aus mul.json laden
with open("mul.json", "r") as f:
    mul_languages = json.load(f)

# Initialisiere ein defaultdict, um die Datenstruktur zu erstellen
language_dict = defaultdict(list)

# Verarbeite die Sprachliste
for lang in mul_languages:
    base_lang = lang.split("_")[0]  # Basis-Sprache extrahieren
    language_dict[base_lang].append(lang)

# Konvertiere defaultdict zu einem normalen Dictionary
language_dict = dict(language_dict)

# Speichere das Ergebnis in einer JSON-Datei
with open("language_mapping.json", "w", encoding="utf-8") as f:
    json.dump(language_dict, f, indent=4, ensure_ascii=False)

print("Umwandlung abgeschlossen. Datei 'language_mapping.json' wurde erstellt.")