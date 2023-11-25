import os 
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox, QFileDialog,QSlider,QVBoxLayout,QLabel,QWidget
import pydicom
from PyQt5.QtGui import QImage, QPixmap
import matplotlib.pyplot as plt
import numpy as np

class Servicio(object):
    def __init__(self):
        self.__usuarios = {}
        #se crea un usuario inicial para arrancar el sistema
        self.__usuarios['bio12345'] = 'medicoAnalitico'
        self.__rutas = []
    
    def verificarUsuario(self, u, c):
        try:
            #Si existe la clave se verifica que sea el usuario
            if self.__usuarios[c] == u:
                return True
            else:
                return False
        except: #si la clave no existe se genera KeyError
            return False
        
    def cargar_senal(self, ruta_carpeta):
        rutas_archivos_dcm = []
        archivos_en_carpeta = os.listdir(ruta_carpeta)
        
        for archivo in archivos_en_carpeta:
            ruta_archivo = os.path.join(ruta_carpeta, archivo)
            rutas_archivos_dcm.append(ruta_archivo)
        if os.path.isfile(ruta_archivo) and archivo.lower().endswith('.dcm'):
            self.__rutas = rutas_archivos_dcm
            return rutas_archivos_dcm
        else:
            print("Formato no válido.")

            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Resultado")
            msg.setText("Archivo no valido")
            msg.show()        
        
    def R_dicom(self,x):
        z=pydicom.dcmread(x)
        matriz=z.pixel_array
        matriz = (matriz / np.max(matriz) * 255).astype(np.uint8)
        altura, ancho = matriz.shape
        imagen_qt = QImage(matriz.data, ancho, altura, ancho, QImage.Format_Grayscale8)
        return imagen_qt
    

    def obtener_informacion_paciente(self, x):
        # Leer el archivo DICOM
        ds = pydicom.dcmread(x)

        # Extraer información del paciente
        informacion_paciente = {
            "PatientName": str(ds.PatientName),
            "PatientID": str(ds.PatientID),
            "BodyPartExamined": str(ds.BodyPartExamined),
            "StudyDescription": str(ds.StudyDescription),
            "StudyDate": str(ds.StudyDate),
        }

        return informacion_paciente
    
    


    


















