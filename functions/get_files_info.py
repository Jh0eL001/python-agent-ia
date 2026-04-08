import os
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

