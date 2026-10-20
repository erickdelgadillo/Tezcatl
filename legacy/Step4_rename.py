import os
from datetime import datetime
import locale
import exifread

# Establecer la configuración regional en español
locale.setlocale(locale.LC_TIME, 'es_ES.utf8')

def get_exif_data(file_path):
    """Obtiene la fecha y hora de captura, y el modelo de cámara desde los datos EXIF."""
    try:
        # Abrir el archivo de imagen en modo binario
        with open(file_path, 'rb') as f:
            # Extraer etiquetas EXIF
            tags = exifread.process_file(f)
            
            # Obtener fecha de captura
            capture_date = None
            if 'EXIF DateTimeOriginal' in tags:
                capture_date = str(tags['EXIF DateTimeOriginal'])
            elif 'Image DateTime' in tags:
                capture_date = str(tags['Image DateTime'])
            
            # Obtener modelo de cámara
            camera_model = None
            if 'Image Model' in tags:
                camera_model = str(tags['Image Model']).replace(" ", "_")  # Reemplazar espacios con guiones bajos
            
            return capture_date, camera_model
    except Exception as e:
        print(f"Error obteniendo datos EXIF para {file_path}: {e}")
        return None, None

def rename_photos_by_model_and_date(root_directory):
    # Almacenar fotos en un diccionario según la fecha de captura
    photos_by_date = {}

    for dirpath, _, filenames in os.walk(root_directory):
        print(f"Explorando directorio: {dirpath}")  # Debugging: print the current directory
        for filename in filenames:
            if filename.lower().endswith(('.jpg', '.jpeg', '.nef')):
                file_path = os.path.join(dirpath, filename)
                print(f"Procesando archivo: {file_path}")  # Debugging: print the current file being processed

                # Obtener la fecha de captura y el modelo de cámara
                capture_date, camera_model = get_exif_data(file_path)

                # Omitir archivos si no se pudo obtener la información requerida
                if capture_date is None or camera_model is None:
                    print(f"No se pudo obtener los datos EXIF necesarios para: {file_path}")
                    continue

                # Formatear la fecha de captura
                try:
                    capture_datetime = datetime.strptime(capture_date, '%Y:%m:%d %H:%M:%S')
                    date_str = capture_datetime.strftime('%d_%m_%Y')
                    
                    # Almacenar fotos en el diccionario según la fecha
                    if date_str not in photos_by_date:
                        photos_by_date[date_str] = []
                    photos_by_date[date_str].append((file_path, camera_model, capture_datetime))
                except Exception as e:
                    print(f"Error formateando la fecha de captura para {file_path}: {e}")
                    continue

    # Check if there are photos to rename
    if not photos_by_date:
        print("No se encontraron fotos con datos EXIF válidos.")
        return

    # Renombrar las fotos
    for date_str, photos in photos_by_date.items():
        # Ordenar las fotos por la fecha y hora de captura
        photos.sort(key=lambda x: x[2])
        
        for i, (file_path, camera_model, capture_datetime) in enumerate(photos):
            # Crear un número incremental con 3 dígitos (e.g., 001, 002, 003)
            file_number = f"{i + 1:03}"
            new_filename = f"{camera_model}_{date_str}_{file_number}{os.path.splitext(file_path)[1]}"
            new_file_path = os.path.join(os.path.dirname(file_path), new_filename)
            
            try:
                os.rename(file_path, new_file_path)
                print(f"Renombrado: {file_path} -> {new_file_path}")
            except Exception as e:
                print(f"Error renombrando {file_path}: {e}")

# Uso
directory_path = "E:\\Photos"
rename_photos_by_model_and_date(directory_path)