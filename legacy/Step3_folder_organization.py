# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 13:57:37 2024

@author: erick
"""

import os
import shutil
from datetime import datetime
import locale
import exifread

# Establecer la configuración regional en español
locale.setlocale(locale.LC_TIME, 'es_ES.utf8')

def get_capture_date(file_path):
    """Obtiene la fecha de captura del archivo desde los datos EXIF."""
    try:
        # Abrir el archivo de imagen en modo binario
        with open(file_path, 'rb') as f:
            # Extraer etiquetas EXIF
            tags = exifread.process_file(f)
            
            # Buscar la etiqueta 'EXIF DateTimeOriginal'
            if 'EXIF DateTimeOriginal' in tags:
                return str(tags['EXIF DateTimeOriginal'])
            elif 'Image DateTime' in tags:
                return str(tags['Image DateTime'])
            else:
                return None
    except Exception as e:
        print(f"Error obteniendo la fecha de captura para {file_path}: {e}")
        return None

def rename_file_with_date(file_path, date_str):
    """Renombra el archivo con la fecha añadida al nombre."""
    directory, filename = os.path.split(file_path)
    name, ext = os.path.splitext(filename)
    
    new_filename = f"{name}_{date_str}{ext}"
    new_file_path = os.path.join(directory, new_filename)
    
    try:
        os.rename(file_path, new_file_path)
        print(f"Renombrado: {file_path} -> {new_file_path}")
        return new_file_path
    except Exception as e:
        print(f"Error renombrando {file_path}: {e}")
        return file_path  # Retorna el archivo original si hubo un error

def organize_photos_by_date(root_directory):
    for dirpath, _, filenames in os.walk(root_directory):
        for filename in filenames:
            if filename.lower().endswith(('.jpg', '.jpeg', '.nef')):
                file_path = os.path.join(dirpath, filename)

                # Obtener la fecha de captura del archivo
                capture_date = get_capture_date(file_path)

                # Omitir archivos si no se pudo obtener la fecha de captura
                if capture_date is None:
                    print(f"No se pudo obtener la fecha de captura para: {file_path}")
                    continue

                # Formatear la fecha de captura
                try:
                    capture_datetime = datetime.strptime(capture_date, '%Y:%m:%d %H:%M:%S')
                    date_str = capture_datetime.strftime('%d_%m_%Y')
                except Exception as e:
                    print(f"Error formateando la fecha de captura para {file_path}: {e}")
                    continue

                # Renombrar el archivo con la fecha de captura
                new_file_path = rename_file_with_date(file_path, date_str)

                # Crear las carpetas de destino
                year_folder = capture_datetime.strftime('%Y')  # Carpeta del año
                month_folder = capture_datetime.strftime('%m - %B')  # Carpeta del mes: "01 - enero"
                new_directory = os.path.join(root_directory, year_folder, month_folder)

                if not os.path.exists(new_directory):
                    os.makedirs(new_directory)

                # Mover el archivo renombrado a la nueva carpeta
                final_file_path = os.path.join(new_directory, os.path.basename(new_file_path))
                try:
                    shutil.move(new_file_path, final_file_path)
                    print(f"Movido: {new_file_path} -> {final_file_path}")
                except Exception as e:
                    print(f"Error moviendo {new_file_path}: {e}")

    # Eliminar las carpetas antiguas vacías
    remove_empty_folders(root_directory)

def remove_empty_folders(root_directory):
    """Elimina las carpetas vacías dentro del directorio especificado."""
    for dirpath, dirnames, _ in os.walk(root_directory, topdown=False):
        for dirname in dirnames:
            folder_path = os.path.join(dirpath, dirname)
            # Eliminar la carpeta si está vacía
            if not os.listdir(folder_path):
                try:
                    os.rmdir(folder_path)
                    print(f"Carpeta eliminada: {folder_path}")
                except Exception as e:
                    print(f"Error eliminando la carpeta {folder_path}: {e}")

# Uso
directory_path = "E:\\Photos"
organize_photos_by_date(directory_path)