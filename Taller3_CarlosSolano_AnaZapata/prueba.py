import pydicom

def imprimir_info_dicom(ruta_archivo):
    # Leer el archivo DICOM
    ds = pydicom.dcmread(ruta_archivo)

    # Imprimir información específica
    print("Información específica del archivo DICOM:")
    print(f"Nombre del paciente: {ds.PatientName}")
    print(f"ID del paciente: {ds.PatientID}")
    print(f"Parte del cuerpo examinada: {ds.BodyPartExamined}")
    print(f"Descripción del estudio: {ds.StudyDescription}")
    print(f"Fecha del estudio: {ds.StudyDate}")

# Ruta de tu archivo DICOM
ruta_archivo_dicom = "C:\\Users\\CARLOS SOLANO\\Desktop\\Trabajo-3-Info-II\\Taller3_CarlosSolano_AnaZapata\\Circle of Willis\\1-001.dcm"

# Llamada a la función para imprimir información
imprimir_info_dicom(ruta_archivo_dicom)

'--------------------------------------------------------------------------------------------------------------'

# ... (tu código existente)

class Vista2(QDialog):
    def __init__(self, ppal=None):
        super().__init__(ppal)
        loadUi("Vista2.ui", self)
        self.__ventanaPadre = ppal
        self.__resultado_lista = []
        self.setup()

    # ... (tu código existente)

    def actualizar_slider(self, value):
        self.nums.setText(str(value))
        self.cargar_imagen()
        self.mostrar_informacion_paciente()  # Agregado para mostrar la información del paciente

    def cargar_imagen(self):
        x = int(self.slider.value())
        x = self.__resultado_lista[x]
        y = self.__controlador.cargar_dicom(x)
        self.mostrar_imagen_en_label(y)

    def mostrar_imagen_en_label(self, imagen_qt):
        pixmap = QPixmap.fromImage(imagen_qt)
        self.img.setScaledContents(True)
        self.img.setPixmap(pixmap)

    def mostrar_informacion_paciente(self):
        x = int(self.slider.value())
        x = self.__resultado_lista[x]
        info_paciente = self.__controlador.obtener_informacion_paciente(x)
        self.nombre.setText(f"Nombre del paciente: {info_paciente['PatientName']}")
        # Agrega más información si es necesario

# ... (tu código existente)
