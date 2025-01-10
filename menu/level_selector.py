import os

def list_levels(mazes_folder="data/mazes/"):
    """
    Argumentos:
        mazes_folder (str): Carpeta donde se encuentran los archivos de laberintos
    Descripción:
        Recorre la carpeta 'mazes_folder' y devuelve una lista con los nombres
        de archivos .txt que haya.
    Salidas:
        levels (list of str): Lista con los nombres de archivo disponibles
    """
    levels = []
    for filename in os.listdir(mazes_folder):
        if filename.endswith(".txt"):
            levels.append(filename)
    return levels
