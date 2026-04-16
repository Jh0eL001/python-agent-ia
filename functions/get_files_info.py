import os
from google.genai import types # no recuerdo
def get_files_info(working_directory, directory="."):
    try:
        # 1. Obtenemos la ruta absoluta de la base (la frontera)
        working_dir_abs = os.path.abspath(working_directory)

        # 2. Construimos la ruta destino y la "normalizamos" (quita los .. y cosas raras)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        # 3. SEGURIDAD: ¿El camino común entre la base y el destino sigue siendo la base?
        # Usamos una lista [] dentro de commonpath
        common = os.path.commonpath([working_dir_abs, target_dir])

        if common != working_dir_abs:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # 4. VALIDACIÓN: ¿Es realmente una carpeta lo que estamos mirando?
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        # Iterate over the items in target directory
        items = os.listdir(target_dir) # asumo que devuelve una lista?
        lines = []
        for item in items:
            # Construimos la ruta completa hasta el dir o file
            item_path = os.path.join(target_dir, item)
            # file size in bytes
            file_size = os.path.getsize(item_path)
            # verificamos si es dir
            is_dir = os.path.isdir(item_path)
            line = f"- {item}: file_size={file_size} bytes, is_dir={is_dir}"
            lines.append(line)
        return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"

# HOW TO TALK WITH GEMINI API
schema_get_files_info = types.FunctionDeclaration(
        name = "get_files_info",
        description = "Lists files in a specified directory relative to the working directory.",
        parameters = types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="Directory path to list files from, relative to the working directory.",
                ),
            },
        ),
)

# Herramienta para leer contenido
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a specific file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read, relative to the working directory."
            ),
        },
        required=["file_path"]
    ),
)

# Herramienta para ejecutar código Python
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file with optional command-line arguments.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute."
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="Optional command-line arguments to pass to the script."
            ),
        },
        required=["file_path"]
    ),
)

# Herramienta para escribir o crear archivos
schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Creates or overwrites a file with the specified content.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path where the file will be written."
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The text content to write into the file."
            ),
        },
        required=["file_path", "content"]
    ),
)
