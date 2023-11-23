
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
        archivoCargado = QFileDialog.getOpenFileName(self, "Abrir señal","","Archivos comprimidos (*.rar),Todos los archivos (*)")
        # Obtener el primer elemento de la tupla que es el nombre del archivo
        archivoCargado = archivoCargado[0]

        

        # Verificar si se seleccionó un archivo y si termina con ".rar" o ".zip"
        if archivoCargado and (archivoCargado.endswith(".rar") or archivoCargado.endswith(".zip")):
            # Aquí puedes realizar las acciones que necesitas con el archivo cargado
            print(f"Archivo cargado exitosamente!!!")

            with rarfile.RarFile(archivoCargado) as rar_ref:
                listaArchivosNombres = rar_ref.namelist()

                visualizar = listaArchivosNombres[0]

                nombre_archivo_sin_extension = os.path.splitext(os.path.basename(archivoCargado))[0]

                # Crear un directorio para extraer el contenido del RAR
                directorio_destino = os.path.join(os.path.dirname(archivoCargado), nombre_archivo_sin_extension)
                os.makedirs(directorio_destino, exist_ok=True)

                # Extraer el contenido en el directorio creado
                rar_ref.extract(visualizar, directorio_destino)

                # Graficar el contenido del archivo DICOM
                plt.imshow(visualizar.pixel_array, cmap=plt.cm.bone)
                plt.title(f"Imagen DICOM: {visualizar}")
                plt.show()

        else:
            print("Formato no válido.")

            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Resultado")
            msg.setText("Archivo no valido")
            msg.show()
            
        print (listaArchivosNombres[0])
        