from modelo.alumno import Alumno

class AsistenciaController:
    def __init__(self, vista):
        self.vista = vista
        self.lista_alumnos = []

    def registrarAsistencia(self, e):

        # Obtener los valores
        nombre = self.vista.txt_nombre.value
        grupo = self.vista.txt_grupo.value
        materia = self.vista.txt_materia.value
        presente = self.vista.chk_presente.value

        # Validar campos vacíos
        if nombre == "" or grupo == "" or materia == "":
            self.vista.lbl_mensaje.value = "Faltan datos por llenar"
            self.vista.lbl_mensaje.color = "red"
            self.vista.page.update()
            return

        # Validar longitud
        if(len(nombre) > 10):
            raise Exception("El nombre del alumno no debe exceder 10 caracteres")

        alumno = Alumno(nombre, presente)

        self.lista_alumnos.append(alumno)

        # Mostrar listado
        self.vista.lista_registros.controls.append(
            self.vista.agregar_Texto(
                f"{grupo} | {materia} | {str(alumno)}"
            )
        )

        self.vista.lbl_mensaje.value = "Asistencia registrada exitosamente"
        self.vista.lbl_mensaje.color = "green"

        # Limpiar solo datos del alumno
        self.vista.txt_nombre.value = ""
        self.vista.chk_presente.value = False

        self.vista.page.update()

    def limpiarCampos(self, e):

        # Limpiar campos
        self.vista.txt_nombre.value = ""
        self.vista.txt_grupo.value = ""
        self.vista.txt_materia.value = ""
        self.vista.chk_presente.value = False

        # Vaciar lista visual
        self.vista.lista_registros.controls.clear()

        # Vaciar lista lógica
        self.lista_alumnos.clear()

        # Mensaje
        self.vista.lbl_mensaje.value = "Nueva clase iniciada"
        self.vista.lbl_mensaje.color = "blue"

        self.vista.page.update()