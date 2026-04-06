from docx import Document
from collections import Counter
import re

# === CONFIGURA AQUÍ EL NOMBRE DE TU ARCHIVO WORD ===
archivo_word = "Word.docx"

# Palabras vacías comunes que no aportan mucho significado
stopwords = {
    "de", "la", "el", "en", "y", "a", "los", "del", "se", "las", "por", "un",
    "para", "con", "no", "una", "su", "al", "lo", "como", "más", "pero", "sus",
    "le", "ya", "o", "este", "sí", "porque", "esta", "entre", "cuando", "muy",
    "sin", "sobre", "también", "me", "hasta", "hay", "donde", "quien", "desde",
    "todo", "nos", "durante", "todos", "uno", "les", "ni", "contra", "otros",
    "ese", "eso", "ante", "ellos", "e", "esto", "mí", "antes", "algunos", "qué",
    "unos", "yo", "otro", "otras", "otra", "él", "tanto", "esa", "estos", "mucho",
    "quienes", "nada", "muchos", "cual", "poco", "ella", "estar", "estas", "algunas",
    "algo", "nosotros", "mi", "mis", "tú", "te", "ti", "tu", "tus", "ellas", "nosotras"
}

def leer_documento(ruta):
    doc = Document(ruta)
    texto = []
    for p in doc.paragraphs:
        if p.text.strip():
            texto.append(p.text.strip())
    return "\n".join(texto)

def dividir_en_oraciones(texto):
    oraciones = re.split(r'(?<=[.!?])\s+', texto)
    return [o.strip() for o in oraciones if o.strip()]

def limpiar_palabras(texto):
    palabras = re.findall(r'\b\w+\b', texto.lower())
    return [p for p in palabras if p not in stopwords and len(p) > 2]

def obtener_palabras_clave(texto, top_n=10):
    palabras = limpiar_palabras(texto)
    conteo = Counter(palabras)
    return conteo.most_common(top_n)

def puntuar_oraciones(oraciones, palabras_frecuentes):
    frecuencia = dict(palabras_frecuentes)
    puntajes = []

    for oracion in oraciones:
        palabras = limpiar_palabras(oracion)
        puntaje = sum(frecuencia.get(p, 0) for p in palabras)
        puntajes.append((oracion, puntaje))

    puntajes.sort(key=lambda x: x[1], reverse=True)
    return puntajes

def main():
    try:
        texto = leer_documento(archivo_word)

        if not texto.strip():
            print("El documento está vacío.")
            return

        oraciones = dividir_en_oraciones(texto)
        palabras_clave = obtener_palabras_clave(texto, top_n=10)
        resumen = puntuar_oraciones(oraciones, palabras_clave)[:5]

        print("\n=== TEXTO EXTRAÍDO ===\n")
        print(texto[:1500])  # muestra solo una parte si es largo

        print("\n=== PALABRAS CLAVE ===\n")
        for palabra, cantidad in palabras_clave:
            print(f"{palabra}: {cantidad}")

        print("\n=== ORACIONES MÁS RELEVANTES ===\n")
        for i, (oracion, puntaje) in enumerate(resumen, 1):
            print(f"{i}. {oracion} (puntaje: {puntaje})")

    except FileNotFoundError:
        print(f"No se encontró el archivo: {archivo_word}")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

if __name__ == "__main__":
    main()