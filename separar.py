import re
from collections import defaultdict

def agrupar_speakers(texto):
    grupos = defaultdict(list)

    patron = r'\[\d{2}:\d{2}\]\s*(Speaker\s+\d+):\s*(.*)'

    for linea in texto.splitlines():
        match = re.match(patron, linea)
        if match:
            speaker, contenido = match.groups()
            grupos[speaker].append(contenido.strip())

    return grupos


with open("transcripcion.txt", "r", encoding="utf-8") as f:
    texto = f.read()

resultado = agrupar_speakers(texto)

with open("transcripcion_agrupada.txt", "w", encoding="utf-8") as f:
    for speaker, textos in resultado.items():
        f.write(f"{speaker}:\n")
        f.write("\n\n".join(textos) + "\n\n")
        f.write("-" * 40 + "\n\n")

print("Listo")