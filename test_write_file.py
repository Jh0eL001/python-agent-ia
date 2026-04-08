from functions.write_file import write_file

# Caso 1: Sobreescribir un archivo existente
print(write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum"))

# Caso 2: Crear un archivo en una subcarpeta nueva
print(write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"))

# Caso 3: Error de seguridad (fuera del directorio)
print(write_file("calculator", "/tmp/temp.txt", "this should not be allowed"))
