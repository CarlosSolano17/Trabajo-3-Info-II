
# Importar librerias básicas
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QMessageBox, QFileDialog,QSlider,QVBoxLayout,QLabel,QWidget
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIntValidator, QRegExpValidator, QPixmap
from PyQt5.QtCore import Qt,QRegExp
from PyQt5.QtGui import QImage
import sys
import pydicom
import os
import datetime 


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
        #print("Boton presionado")
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
        ventana_ingreso.asignarControlador(self.__controlador)
        self.hide()
        ventana_ingreso.show()

class Vista2(QDialog):
    def __init__(self, ppal=None):
        super().__init__(ppal)
        loadUi("Vista2.ui",self)
        self.__ventanaPadre = ppal
        self.__resultado_lista = []
        self.setup()

    #metodo para configurar las senales-slots y otros de la interfaz
    def setup(self):
        #se programa la senal para el boton
        self.BotonSalir.clicked.connect(self.accionSalir)
        self.cargar.clicked.connect(self.cargarSenal)
        self.slider.valueChanged.connect(self.actualizar_slider)

    def asignarControlador(self,c):
        self.__controlador = c

    def accionSalir(self):
        #print("Boton presionado Salir")
        self.hide()
        self.__ventanaPadre.show()

    #Se le pide al usuario que ingrese una carpeta y esta verifica que todos los datos de la carpeta sean archivos .dcm 
    def cargarSenal(self):
        ruta_carpeta = QFileDialog.getExistingDirectory(self, 'Seleccionar Carpeta', '/')
        self.__resultado_lista = self.__controlador.cargar_senal_desde_carpeta(ruta_carpeta)
        self.configurar_rango_slider()
        return ruta_carpeta
    
    #El rango del slider va a hacer :el len de la carpeta con los archivos .dcm y va pasando uno por uno 
    def configurar_rango_slider(self):
        num_elementos = len(self.__resultado_lista)
        self.slider.setRange(0, num_elementos - 1)
        self.slider.setSingleStep(1)

    # Muestra en la vista el numero de la imagen cuando el slider va pasando 
    def actualizar_slider(self,value):
      self.nums.setText(str(value))
      self.cargar_imagen()
      self.mostrar_informacion_paciente()

    def cargar_imagen(self):
        x = int(self.slider.value())
        x = self.__resultado_lista[x]
        y= self.__controlador.cargar_dicom(x)
        self.mostrar_imagen_en_label(y)

    # Mostrar la imagen en el QLabel llamado 'img'
    def mostrar_imagen_en_label(self, imagen_qt):
        pixmap = QPixmap.fromImage(imagen_qt)
        self.img.setScaledContents(True)
        self.img.setPixmap(pixmap)
    

    def mostrar_informacion_paciente(self):
        x = int(self.slider.value())
        x = self.__resultado_lista[x]
        info_paciente = self.__controlador.extraerInfo(x)
        fecha_estudio = datetime.datetime.strptime(info_paciente['StudyDate'], '%Y%m%d').strftime('%d-%m-%Y')
        self.nombre.setText(f"{info_paciente['PatientName']}")
        self.id.setText(f"{info_paciente['PatientID']}")
        self.partecuerpo.setText(f"{info_paciente['BodyPartExamined']}")
        self.estudio.setText(f"{info_paciente['StudyDescription']}")
        self.fecha.setText(f"{fecha_estudio}")