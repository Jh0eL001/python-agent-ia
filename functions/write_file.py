import os

def write_file(working_directory, file_path, content):
    try:
        # 1. Validaciones de ruta
        working_directory_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_directory_abs, file_path))
        common = os.path.commonpath([working_directory_abs, target_file])

        if common != working_directory_abs:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        # 2. Preparación de carpetas (dirname y makedirs)
        parent_dir = os.path.dirname(target_file)
        os.makedirs(parent_dir, exist_ok=True)

        # 3. Escritura real
        with open(target_file, "w", encoding='utf-8') as f:
            f.write(content)

        # IMPORTANTE: El return para avisar que todo salió bien
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        # Si algo falla (permisos, disco lleno, etc.), devolvemos el error
        return f"Error: {e}"
