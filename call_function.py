from google.genai import types
# 1. Importamos las funciones reales
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file

# 2. Definimos los ESQUEMAS para que Gemini entienda las herramientas
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from.",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads the content of a specific file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the file to read.",
            ),
        },
        required=["file_path"]
    ),
)

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
                description="Optional arguments."
            ),
        },
        required=["file_path"]
    ),
)

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
                description="The text content to write."
            ),
        },
        required=["file_path", "content"]
    ),
)

# 3. La "Caja de Herramientas" que enviamos a la API
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ],
)

# 4. El Mapa que usa Python para ejecutar la función real
function_map = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "run_python_file": run_python_file,
    "write_file": write_file,
}

# 5. La lógica de despacho (Dispatch logic)
def call_function(function_call, verbose=False):
    function_name = function_call.name or ""
    
    if verbose:
        print(f"Calling function: {function_name}({function_call.args})")
    else:
        print(f" - Calling function: {function_name}")

    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[types.Part.from_function_response(
                name=function_name,
                response={"error": f"Unknown function: {function_name}"},
            )],
        )

    args = dict(function_call.args) if function_call.args else {}
    args["working_directory"] = "./calculator"

    try:
        function_result = function_map[function_name](**args)
    except Exception as e:
        function_result = f"Error: {e}"

    return types.Content(
        role="tool",
        parts=[types.Part.from_function_response(
            name=function_name,
            response={"result": function_result},
        )],
    )
