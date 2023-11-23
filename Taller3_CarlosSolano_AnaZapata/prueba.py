import os
import pydicom
import matplotlib.pyplot as plt

def visualizar_archivos_dicom(ruta_carpeta_dicom):
    # Obtener la lista de archivos DICOM en la carpeta
    archivos_dicom = [archivo for archivo in os.listdir(ruta_carpeta_dicom) if archivo.endswith(".dcm")]

    # Iterar sobre cada archivo DICOM y mostrarlo
    for archivo in archivos_dicom:
        ruta_archivo_dicom = os.path.join(ruta_carpeta_dicom, archivo)
        archivo_dicom = pydicom.dcmread(ruta_archivo_dicom)

        # Obtener la imagen DICOM como un array NumPy
        imagen_dicom = archivo_dicom.pixel_array

        # Mostrar la imagen utilizando matplotlib
        plt.imshow(imagen_dicom, cmap='gray')  # cmap='gray' para mostrar en escala de grises
        plt.title(f'Imagen DICOM: {archivo}')
        plt.axis('off')  # Desactivar los ejes si no son necesarios
        plt.show()

# Ruta a la carpeta que contiene los archivos DICOM
ruta_carpeta_dicom = "C:\\Users\\CARLOS SOLANO\\Desktop\\Trabajo-3-Info-II\\Taller3_CarlosSolano_AnaZapata\\Circle of Willis"

# Llamar a la función para visualizar los archivos DICOM en la carpeta
visualizar_archivos_dicom(ruta_carpeta_dicom)
