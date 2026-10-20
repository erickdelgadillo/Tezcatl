# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 12:13:33 2024

@author: erick
"""

import os

def remove_jpg_if_nef_exists(directory):
    # Obtener todos los archivos en el directorio y sus subdirectorios
    for dirpath, _, filenames in os.walk(directory):
        # Crear sets de archivos .JPG y .NEF (sin extensión)
        jpg_files = {os.path.splitext(f)[0] for f in filenames if f.lower().endswith('.jpg')}
        nef_files = {os.path.splitext(f)[0] for f in filenames if f.lower().endswith('.nef')}
        
        # Encontrar archivos JPG que tienen un equivalente NEF
        jpg_to_remove = jpg_files.intersection(nef_files)

        # Eliminar los archivos JPG que tienen una copia en NEF
        for jpg_base_name in jpg_to_remove:
            jpg_file_path = os.path.join(dirpath, jpg_base_name + '.JPG')
            try:
                os.remove(jpg_file_path)
                print(f"Eliminado: {jpg_file_path}")
            except Exception as e:
                print(f"Error eliminando el archivo {jpg_file_path}: {e}")

# Uso
directory_path = "E:\\Photos"
remove_jpg_if_nef_exists(directory_path)