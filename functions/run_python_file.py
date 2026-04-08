import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        common = os.path.commonpath([working_dir_abs, target_file])

        # VALIDACIONES INICIALES (Requerimiento exacto)
        if common != working_dir_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        # EJECUCIÓN
        command = ["python", target_file]
        if args:
            command.extend(args)

        result = subprocess.run(
            command,
            cwd=working_dir_abs,
            capture_output=True,
            text=True,
            timeout=30
        )

        # CONSTRUCCIÓN DEL STRING DE SALIDA (Sigue este orden exacto)
        output = ""

        # 1. Check returncode
        if result.returncode != 0:
            output += f"Process exited with code {result.returncode}\n"

        # 2. Check if both are empty
        if not result.stdout and not result.stderr:
            output += "No output produced"
        else:
            # 3. Include STDOUT if it exists
            if result.stdout:
                output += f"STDOUT:\n{result.stdout}"
            # 4. Include STDERR if it exists
            if result.stderr:
                # Añadimos un salto de línea si ya hay algo en el output
                if output and not output.endswith("\n"):
                    output += "\n"
                output += f"STDERR:\n{result.stderr}"

        return output.strip() # .strip() para limpiar saltos de línea accidentales al final

    except Exception as e:
        return f"Error: executing Python file: {e}"
