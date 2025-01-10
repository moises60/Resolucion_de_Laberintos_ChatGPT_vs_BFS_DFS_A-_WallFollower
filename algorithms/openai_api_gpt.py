import openai
from utils.config import API_KEY

def solve_with_openai_gpt(maze, start, goal):
    """
    Argumentos:
        maze (Maze): Laberinto con .rows, .cols y .grid (0=pasillo, 1=pared)
        start (tuple): (row, col) de inicio
        goal (tuple): (row, col) de meta
    Descripción:
        Envía la descripción del laberinto a la API de OpenAI (ChatCompletion)
        para que devuelva exclusivamente la ruta en formato Python parseable:
          [(r1, c1), (r2, c2), ..., (rN, cN)]
        Si no hay ruta, debe responder `None`
    Salidas:
        path (list of (int,int)) o None
    """
    # 1. Configurar la clave de OpenAI
    openai.api_key = API_KEY
    if not API_KEY:
        print("No se ha definido API_KEY. Revisa config.py o variables de entorno.")
        return None
    
    # 2. Convertir la matriz del laberinto a texto
    #    (Cada fila separada por salto de línea ,ada valor separado por espacio)
    grid_text = "\n".join(
        " ".join(str(cell) for cell in row)
        for row in maze.grid
    )

    # 3. Construir el mensaje para ChatCompletion
    messages = [
        {
            "role": "system",
            "content": "Eres un experto en encontrar rutas en laberintos."
        },
        {
            "role": "user",
            "content": f"""
Tengo un laberinto de {maze.rows} filas y {maze.cols} columnas,
con 0 = pasillo y 1 = pared.

La matriz es:
{grid_text}

La posición de inicio (row, col) es {start}.
La meta (row, col) es {goal}.

Devuélveme ÚNICAMENTE la lista de celdas en formato Python parseable,
por ejemplo: [(6,3),(6,4),(6,5),(6,6)].
No incluyas explicaciones, ni código extra.

Si no hay ruta posible, responde EXACTAMENTE: None
"""
        }
    ]

    try:
        # 4. Llamada a la API de Chat (GPT-4, GPT-3.5-turbo, etc.)
        response = openai.ChatCompletion.create(
            model="gpt-4o",        # Ajusta eñ modelo 
            messages=messages,
            max_tokens=800,
            temperature=0
        )

        # 5. Extraer la respuesta del asistente
        answer = response.choices[0].message.content.strip()
        print("Respuesta de OpenAI:", answer)

        # 6. Comprobar si la respuesta es "None"
        if answer == "None":
            return None

        # 7. Intentar parsear con eval
        try:
            path = eval(answer)  
            # 8. Validar que sea lista de tuplas
            if isinstance(path, list) and all(isinstance(p, tuple) for p in path):
                return path
            else:
                print("El formato devuelto no es una lista de tuplas.")
                return None
        except:
            print("No se pudo parsear la respuesta de OpenAI.")
            return None

    except Exception as e:
        print("Error al llamar a OpenAI:", e)
        return None
