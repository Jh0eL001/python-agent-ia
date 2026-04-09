from google.genai import types # no recuerdo
from functions.get_files_info import schema_get_files_info
available_functions = types.Tool(
    function_declarations=[schema_get_files_info],
)
