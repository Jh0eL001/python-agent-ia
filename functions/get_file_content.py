import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        # 1. Obtenemos la ruta absoluta de la base (la frontera)
        working_dir_abs = os.path.abspath(working_directory)

        # 2. Construimos la ruta destino y la "normalizamos" (quita los .. y cosas raras)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # 3. SEGURIDAD: ¿El camino común entre la base y el destino sigue siendo la base?
        # Usamos una lista [] dentro de commonpath
        common = os.path.commonpath([working_dir_abs, target_file])

        if common != working_dir_abs:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # 4. VALIDACIÓN: ¿Es realmente un archivo lo que estamos mirando?
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        #5. LECTURA del archivo a un maximo de 1000 char

        with open(target_file, "r", encoding='utf-8') as f:
            content = f.read(MAX_CHARS)

            # After reading the first MAX_CHARS...
            if f.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return content
    except Exception as e:
        return f"Error: {e}" 
