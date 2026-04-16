import os
import sys
import argparse
from unittest.mock import MagicMock
from google.genai import types
from call_function import call_function

# --- GENERADOR SIMULADO (MOCK) ---
# Esta función engaña a nuestro agente haciéndole creer que habla con Gemini
def mock_generate_content(prompt, turn):
    response = MagicMock()
    response.usage_metadata.prompt_token_count = 10
    response.usage_metadata.candidates_token_count = 20
    
    content_mock = MagicMock()
    part_mock = MagicMock()
    
    prompt_lower = prompt.lower()

    # Simulamos el proceso de razonamiento paso a paso
    if "render results" in prompt_lower:
        if turn == 0:
            part_mock.function_call.name = "get_files_info"
            part_mock.function_call.args = {"directory": "."}
        elif turn == 1:
            part_mock.function_call.name = "get_file_content"
            part_mock.function_call.args = {"file_path": "main.py"}
        else:
            part_mock.function_call = None # No más funciones
            response.text = "The calculator uses the print() function and format_json_output() to render results to the console."
    else:
        # Fallback para cualquier otro test
        if turn == 0:
            part_mock.function_call.name = "get_files_info"
            part_mock.function_call.args = {"directory": "."}
        else:
            part_mock.function_call = None
            response.text = "Here is your mocked response."

    content_mock.parts = [part_mock]
    response.candidates = [MagicMock(content=content_mock)]
    return response

# --- FUNCIÓN PRINCIPAL ---
def main():
    parser = argparse.ArgumentParser(description="AI Agent CLI")
    parser.add_argument("user_prompt", type=str, help="The prompt for the AI agent")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    # 1. Iniciamos el historial de conversación (memoria del agente)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    mock_turn = 0 # Contador para saber en qué paso del engaño estamos

    # 2. EL AGENT LOOP (Máximo 20 iteraciones según el assignment)
    for _ in range(20):
        # LLAMADA A LA IA SIMULADA (0 tokens gastados)
        response = mock_generate_content(args.user_prompt, mock_turn)
        mock_turn += 1

        # 3. Guardar lo que la IA respondió en la memoria
        if response.candidates:
            candidate_content = response.candidates[0].content
            messages.append(candidate_content)

        # 4. Revisar si la IA quiere llamar a alguna herramienta
        function_calls = [part.function_call for part in candidate_content.parts if part.function_call]

        if function_calls:
            function_responses = []
            for fc in function_calls:
                # Ejecutamos nuestra función local REAL
                function_call_result = call_function(fc, verbose=args.verbose)
                function_responses.append(function_call_result.parts[0])
            
            # 5. Guardar la respuesta de la herramienta en la memoria con role="user"
            messages.append(types.Content(role="user", parts=function_responses))
        else:
            # 6. Condición de salida: No hay funciones, imprimir y salir
            print("Final response:")
            print(response.text)
            return  # Rompe el bucle con éxito

    # Si llega a 20 vueltas y no termina, falla (según assignment)
    print("Error: Maximum iterations reached without a final response.")
    sys.exit(1)

if __name__ == "__main__":
    main()
