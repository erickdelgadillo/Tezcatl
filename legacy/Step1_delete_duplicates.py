# -*- coding: utf-8 -*-
"""
Editor de Spyder

Este es un archivo temporal.
"""

import os
import hashlib

def calculate_hash(file_path, block_size=65536):
    """Calcula el hash MD5 de un archivo."""
    hash_func = hashlib.md5()
    with open(file_path, 'rb') as file:
        while chunk := file.read(block_size):
            hash_func.update(chunk)
    return hash_func.hexdigest()

def remove_duplicates(directory):
    hashes = {}  # Diccionario para almacenar los hashes de los archivos
    duplicates = []  # Lista para almacenar archivos duplicados

    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)

            try:
                # Calcular el hash del archivo actual
                file_hash = calculate_hash(file_path)

                if file_hash in hashes:
                    # Si el hash ya está en el diccionario, es un duplicado
                    duplicates.append(file_path)
                else:
                    # De lo contrario, añadirlo al diccionario
                    hashes[file_hash] = file_path
            except Exception as e:
                print(f"Error procesando el archivo {file_path}: {e}")

    # Eliminar archivos duplicados
    for file_path in duplicates:
        try:
            os.remove(file_path)
            print(f"Eliminado duplicado: {file_path}")
        except Exception as e:
            print(f"Error eliminando el archivo {file_path}: {e}")

    print(f"Total de duplicados eliminados: {len(duplicates)}")

# Uso
directory_path = "E:\\Photos"
remove_duplicates(directory_path)