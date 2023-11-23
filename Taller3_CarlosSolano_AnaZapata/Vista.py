
# Importar librerias básicas
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox, QFileDialog,QSlider,QVBoxLayout,QLabel,QWidget
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIntValidator, QRegExpValidator, QPixmap
from PyQt5.QtCore import Qt,QRegExp
import matplotlib.pyplot as plt
import sys
import pydicom
import rarfile
import os

class VentanaPrincipal(QMainWindow):
    #constructor
    def __init__(self, ppal=None):
        super(VentanaPrincipal,self).__init__(ppal)
        loadUi('VentanaLogin.ui',self)
        self.setup()

    #metodo para configurar las senales-slots y otros de la interfaz
    def setup(self):
        #se programa la senal para el boton
        self.boton_ingresar.clicked.connect(self.accion_ingresar)


    def asignarControlador(self,c):
        self.__controlador = c

    def accion_ingresar(self):
        print("Boton presionado")
        usuario = self.campo_usuario.text()
        password = self.campo_password.text()

        #esta informacion la debemos pasar al controlador
        resultado = self.__controlador.validar_usuario(usuario,password)

        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Resultado")

        #se selecciona el resultado de acuerdo al resultado de la operacion
        if resultado == True:
            self.abrirVista2()

        else:
            msg.setText("Usuario no Valido")
            msg.show()
            self.campo_usuario.clear()
            self.campo_password.clear()
        
    def abrirVista2(self):
        self.campo_usuario.clear()
        self.campo_password.clear()
        ventana_ingreso=Vista2(self)
        self.hide()
        ventana_ingreso.show()


class Vista2(QDialog):
    def __init__(self, ppal=None):
        super().__init__(ppal)
        loadUi("Vista2.ui",self)
        self.__ventanaPadre = ppal
        self.setup()

    #metodo para configurar las senales-slots y otros de la interfaz
    def setup(self):
        #se programa la senal para el boton
        self.BotonSalir.clicked.connect(self.accionSalir)
        self.cargar.clicked.connect(self.cargarSenal)

    def asignarControlador(self,c):
        self.__controlador = c

    def accionSalir(self):
        print("Boton presionado Salir")
        self.hide()
        self.__ventanaPadre.show()

    def cargarSenal(self):
        ruta_carpeta = QFileDialog.getExistingDirectory(self, 'Seleccionar Carpeta', '/')

        archivos_en_carpeta = os.listdir(ruta_carpeta)
        todos_dcm = all(archivo.endswith(".dcm") for archivo in archivos_en_carpeta)

        if todos_dcm:
            print(f"Archivo cargado exitosamente!!!")
            

        else:
            print("Formato no válido.")

            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Resultado")
            msg.setText("Archivo no valido")
            msg.show()



    def obtener_primera_imagen_dicom(self, ruta_carpeta):
        archivos_dicom = [archivo for archivo in os.listdir(ruta_carpeta) if archivo.endswith(".dcm")]
        if archivos_dicom:
            ruta_primera_imagen = os.path.join(ruta_carpeta, archivos_dicom[0])
            imagen_dicom = pydicom.dcmread(ruta_primera_imagen).pixel_array
            print(imagen_dicom)
            return imagen_dicom
        
        else:
            return None

    
