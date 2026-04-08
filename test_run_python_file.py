from functions.run_python_file import run_python_file

# Caso 1: Instrucciones de uso
print(run_python_file("calculator", "main.py"))

# Caso 2: Operación real
print(run_python_file("calculator", "main.py", ["3 + 5"]))

# Caso 3: Ejecutar los tests internos de la calculadora
print(run_python_file("calculator", "tests.py"))

# Caso 4: Error de seguridad (fuera del directorio)
print(run_python_file("calculator", "../main.py"))

# Caso 5: Error de existencia
print(run_python_file("calculator", "nonexistent.py"))

# Caso 6: Error de extensión
print(run_python_file("calculator", "lorem.txt"))
