from functions.get_file_content import get_file_content
from config import MAX_CHARS

# --- 1. Test de Truncado (lorem.txt) ---
print(f"--- Testing get_file_content('calculator', 'lorem.txt') ---")
result_lorem = get_file_content("calculator", "lorem.txt")

# Verificamos si se truncó comparando el largo
print(f"Total characters received: {len(result_lorem)}")
if f'truncated at {MAX_CHARS} characters' in result_lorem:
    print("Result: OK (File was truncated correctly)")
    # Imprimimos solo el final para ver el mensaje
    print(f"End of string: ...{result_lorem[-100:]}")
else:
    print("Result: File was not truncated (maybe it's smaller than MAX_CHARS?)")

# --- 2. Test de archivos normales ---
print("\n--- Testing get_file_content('calculator', 'main.py') ---")
print(get_file_content("calculator", "main.py"))

print("\n--- Testing get_file_content('calculator', 'pkg/calculator.py') ---")
print(get_file_content("calculator", "pkg/calculator.py"))

# --- 3. Test de Errores (Seguridad y Existencia) ---
print("\n--- Testing get_file_content('calculator', '/bin/cat') ---")
print(get_file_content("calculator", "/bin/cat"))

print("\n--- Testing get_file_content('calculator', 'pkg/does_not_exist.py') ---")
print(get_file_content("calculator", "pkg/does_not_exist.py"))
