import openai
from utils.config import API_KEY

def solve_with_openai_o1(maze, start, goal):
    """
    Argumentos:
        maze (Maze): Laberinto con .rows, .cols, .grid (0=pasillo, 1=pared)
        start (tuple): (row, col) de inicio
        goal (tuple): (row, col) de meta
    Descripción:
        Envía la descripción del laberinto a la API de OpenAI (modelo 'o1-mini' 
        o similar), usando ChatCompletion pero sin role="system"
        El prompt indica que devuelva únicamente la lista de celdas en 
        formato Python parseable (o 'None').
    Salidas:
        path (list of (int,int)) o None
    """
    # 1. Configurar la clave de OpenAI
    openai.api_key = API_KEY
    if not API_KEY:
        print("No se ha definido API_KEY. Revisa config.py o variables de entorno.")
        return None

    # 2. Convertir la matriz del laberinto a texto
    grid_text = "\n".join(
        " ".join(str(cell) for cell in row)
        for row in maze.grid
    )

    # 3. Construir el mensaje "user" sin "system"
    messages = [
        {
            "role": "user",
            "content": f"""
Tengo un laberinto de {maze.rows} filas y {maze.cols} columnas,
con 0 = pasillo y 1 = pared.

La matriz es:
{grid_text}

La posición de inicio (row, col) es {start}
La meta (row, col) es {goal}

Por favor, devuélveme una lista en Python parseable con las celdas (r, c)
desde 'start' hasta 'goal', moviéndose solo en celdas con 0
hacia arriba/abajo/izquierda/derecha, por ejemplo:
[(r1, c1), (r2, c2), ..., (rN, cN)]

Si no hay ruta, responde exactamente 'None'.

No incluyas explicaciones ni código adicional.
"""
        }
    ]

    try:
        # 4. Llamada a la API Chat con "o1" 
        response = openai.ChatCompletion.create(
            model="o1-mini",     
            messages=messages, 
            max_completion_tokens=800,
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
                print("El formato de la respuesta no es una lista de tuplas.")
                return None
        except:
            print("No se pudo parsear la respuesta de OpenAI.")
            return None

    except Exception as e:
        print("Error al llamar a OpenAI:", e)
        return None
