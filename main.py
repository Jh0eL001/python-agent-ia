import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

# --- 1. FUNCIÓN DE GENERACIÓN ---
def generate_content(client, messages):
    response = client.models.generate_content(
        model='gemini-2.0-flash',
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
            temperature=0
        ),
    )
    if response.usage_metadata is None:
        raise RuntimeError("Invalid API response: Missing usage_metadata.")
    return response

# --- 2. FUNCIÓN PRINCIPAL ---
def main():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    # Configuración de Argparse
    parser = argparse.ArgumentParser(description="AI Agent CLI")
    parser.add_argument("user_prompt", type=str, help="The prompt for the AI agent")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY no encontrada en el entorno")

    # Inicialización del cliente
    client = genai.Client(api_key=api_key)

    # Preparamos el mensaje inicial del usuario
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    # Llamamos a la IA
    response = generate_content(client, messages)
    usage = response.usage_metadata

    # Lógica Verbose para tokens
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {usage.prompt_token_count}")
        print(f"Response tokens: {usage.candidates_token_count}")

    # Procesamos la respuesta del modelo
    content = response.candidates[0].content
    # Extraemos todas las llamadas a funciones de las 'parts'
    function_calls = [part.function_call for part in content.parts if part.function_call]

    print("Response:")

    if function_calls:
        function_results = []
        for fc in function_calls:
            # Ejecutamos la función físicamente en nuestra máquina
            function_call_result = call_function(fc, verbose=args.verbose)

            # Validaciones de seguridad de Boot.dev
            if not function_call_result.parts:
                raise RuntimeError("Function call result has no parts.")

            f_res = function_call_result.parts[0].function_response
            if f_res is None:
                raise RuntimeError("FunctionResponse is None.")
            if f_res.response is None:
                raise RuntimeError("FunctionResponse.response is None.")

            # Guardamos el resultado (se usará en el siguiente sprint para el loop)
            function_results.append(function_call_result.parts[0])

            # En modo verbose imprimimos el retorno de la función de Python
            if args.verbose:
                print(f"-> {f_res.response}")
    else:
        # Si no hubo intención de usar herramientas, imprimimos el texto de la IA
        print(response.text)

if __name__ == "__main__":
    main()
