from flask import Flask, request, jsonify
from flask_cors import CORS
import anthropic
import os

app = Flask(__name__)
CORS(app)

TRANSCRIPT = """
Hola, bienvenidos al taller de cómo sacar un patrón a través de una prenda ya hecha. Yo soy Diana Samayoa, cofundadora de Estudio 2. Comencemos.

Los materiales que estaremos usando son los siguientes. Una prenda que quiera sacar, ya sea un pantalón, blusa, falda, tijeras, pegamento o cualquier tape en el que le puedas escribir encima, sea esta cinta mágica o masking tape, cinta métrica, lápiz o portaminas, Curva de bocamanga. Si estás haciendo blusas o una curva de caderas, está haciendo faldas o pantalones. Borrador. Una citrus que es una regla de patronaje, alfileres y papel de tu preferencia, ya sea mantequilla o kraft.

Como primer paso debemos analizar nuestra prenda y ver todas las piezas que lo componen. El pantalón de ejemplo tiene: una bolsa diagonal en el costado, un corte vertical de acceso a la bolsa, pasadores, careta interna, bolsas de parche en la parte de atrás, pinzas, pretina, y ruedo con vista.

Como segundo paso debemos trazar líneas de balance para evitar que la prenda se tuerza. Se mide el largo del pantalón sin contar la pretina, se saca una línea recta. El ruedo del frente mide 7 pulgadas, la mitad 3.5, se saca 3.5 para cada lado y una línea perpendicular de 33.5 pulgadas de largo. El alto del tiro es 8 pulgadas.

Para colocar la prenda: se pone al revés sobre el papel para trazar las costuras. Se usan alfileres para fijarla. El ancho de entrepierna del frente es 1.25 pulgadas, total 5.625. Se jala el exceso de tela de atrás para que el tiro quede al ras. Se traza con lápiz o tiza. Se incluye el corte diagonal de la bolsa y el acceso.

Para la parte trasera: el ancho de tiro es 15 pulgadas (13 visibles + 2 al frente). El ruedo mide 9.5 pulgadas. En la cintura trasera lleva una pinza de 1 pulgada de profundidad (x2 = 2 pulgadas que se agregan). La pinza va a 4.75 pulgadas desde el costado.

Para rectificar medidas: el costado mide 34.25 pulgadas en el trazo y en la prenda real. Si hay diferencia pequeña se corrige en la cintura. Entrepierna frente: 7.125 pulgadas. Entrepierna trasera: 13.125 pulgadas. Largo cintura a ruedo: 35 pulgadas.

La pretina mide 16 pulgadas abajo y 15.5 arriba, grosor 0.625 pulgadas. Va con indicación centro cerrado.

La careta interna mide 6.75 pulgadas de largo por 0.875 de ancho. Va centro cerrado. Se hacen dos versiones: una recta y una con curvatura en la esquina inferior.

Para desglosar en papel mantequilla: se retrasea cada pieza y se agrega 0.5 pulgadas de costura en todos los lados. Al ruedo solo 0.5 pulgadas porque lleva vista.

Rotulación: nombre de la pieza, nombre de la prenda, cantidad a cortar, dirección del hilo tela, y si va centro cerrado.

Las piezas del frente son tres: pierna del frente (x2), bolsa superior (x2), bolsa inferior con fondo y vista (x2).

Vista del ruedo: 2.125 pulgadas de ancho. Frente x2 y espalda x2.

Pasadores: 2.25 pulgadas de largo x 0.75 de ancho, con 0.375 de doblez en cada extremo y 0.25 de costura en los lados.

Al terminar de calcar todas las piezas se cortan en papel y luego en tela. Si no eres quien va a coser, todas las piezas deben ir correctamente rotuladas.
"""

SYSTEM_PROMPT = f"""Eres HilvanaBot, el asistente del taller "Cómo sacar un patrón de una prenda hecha" de la plataforma educativa Hilvana. La instructora es Diana Samayoa, cofundadora de Estudio 2.

Tu única fuente de información es la transcripción del video de este taller que se incluye abajo. Responde EXCLUSIVAMENTE con base en esa transcripción. Si la respuesta no está en la transcripción, di exactamente: "Esa información no se menciona en este taller. Te recomiendo revisar el video o consultar a la instructora Diana."

No uses conocimiento general de patronaje o moda fuera de lo que dice la transcripción. No inventes pasos, materiales ni medidas. Si preguntan de otro taller, indica que ese tema pertenece a otro taller de Hilvana.

Responde siempre en español, de forma amigable y clara para jóvenes de 14 a 18 años. Sé breve y directo.

--- TRANSCRIPCIÓN DEL TALLER ---
{TRANSCRIPT}
--- FIN DE TRANSCRIPCIÓN ---"""

@app.route("/hilvanabot", methods=["POST"])
def hilvanabot():
    data = request.get_json()
    message = data.get("message", "")
    if not message:
        return jsonify({"error": "No se recibió mensaje"}), 400
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=400,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": message}]
    )
    return jsonify({"reply": response.content[0].text})

@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "HilvanaBot activo"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
