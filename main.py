import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

# --- 1. FUNCIÓN REFACTORIZADA ---
# Esta función ahora es un "trabajador silencioso".
# Solo hace la llamada y devuelve el objeto completo.
def generate_content(client, messages):
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=messages
    )
    # Validamos que la respuesta tenga metadata (importante para el backend)
    if response.usage_metadata is None:
        raise RuntimeError("Invalid API response: Missing usage_metadata.")
    return response

# --- 2. FUNCIÓN PRINCIPAL ---
def main():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    # Configuración de Argparse
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY no encontrada en el entorno")

    # Inicialización del cliente
    client = genai.Client(api_key=api_key)

    # Preparamos el mensaje usando los types de la API
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    # Llamamos a la función que refactorizamos
    response = generate_content(client, messages)
    usage = response.usage_metadata

    # --- LÓGICA DEL ASSIGNMENT (VERBOSE) ---
    # Si el usuario puso --verbose, imprimimos el prompt y los tokens.
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {usage.prompt_token_count}")
        print(f"Response tokens: {usage.candidates_token_count}")

    # Esto se imprime SIEMPRE (tengas verbose o no)
    print("Response:")
    print(response.text)

if __name__ == "__main__":
    main()
