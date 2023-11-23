import pydicom
import matplotlib.pyplot as plt

ruta_dicom = "C:\\Users\\CARLOS SOLANO\\Desktop\\Trabajo-3-Info-II\\Taller3_CarlosSolano_AnaZapata\\Circle of Willis\\1-001.dcm"

# Leer el archivo DICOM
archivo_dicom = pydicom.dcmread(ruta_dicom)

# Acceder a la imagen DICOM como un array NumPy
imagen_dicom = archivo_dicom.pixel_array

# Mostrar la imagen utilizando matplotlib
plt.imshow(imagen_dicom, cmap='gray')  # cmap='gray' para mostrar en escala de grises
plt.title('Imagen DICOM')
plt.axis('off')  # Desactivar los ejes si no son necesarios
plt.show()
