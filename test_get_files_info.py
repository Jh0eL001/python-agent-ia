from functions.get_files_info import get_files_info
'''Python busca una carpeta llamada functions y dentro un archivo
llamado get_file_info.py. No necesitas poner el .py porque Python
ya sabe que está buscando un archivo de código'''

# TESTS
print("Result for current directory:")
print(get_files_info("calculator", "."))

print("Result for 'pkg' directory:")
print(get_files_info("calculator", "pkg"))

print("Result for '/bin' directory:")
print(get_files_info("calculator", "/bin"))

print("Result for '../' directory:")
print(get_files_info("calculator", "../"))
