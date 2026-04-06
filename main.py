import os
from dotenv import load_dotenv
from google import genai

def main():
    # 1. Cargar las variables del archivo .env
    load_dotenv()
    # 2. Obtener la API KEY del entorno
    api_key = os.getenv("GEMINI_API_KEY")
    prompt = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    # 3. Validar que la llave exista
    if api_key is None:
        raise RuntimeError("GEMINI_API_KEY no encontrada en el entorno")

    print("¡Conexión configurada exitosamente!")
    # Aquí irá luego la lógica de tu Agente
    # creamos una instancia creo
    client = genai.Client(api_key=api_key)
    # usamos la instancia para comunicarnos con la API de gemini
    response = client.models.generate_content(
            model='gemini-2.5-flash', contents= prompt
    )
    # vemos cuantos tokens cobra gemini jaja
    usage = response.usage_metadata # aca para acceder a la metadata
    print(f"User prompt: {prompt}")
    if usage is not None:
        print(f"Prompt tokens: {usage.prompt_token_count}")
        print(f"Response tokens: {usage.candidates_token_count}")
        print(f"Response:\n{response.text}")
    else:
        raise RuntimeError("Invalid API response: Missing usage_metadata.")
if __name__ == "__main__":
    main()
