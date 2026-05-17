import flet as ft

class AsistenciaView:
    def __init__(self, page: ft.Page):

        self.page = page

        self.page.title = "Sistema de asistencia"
        self.page.window_width = 500
        self.page.window_height = 650
        self.page.padding = 20

        self.txt_grupo = ft.TextField(
            label="Grupo",
            width=400
        )

        self.txt_materia = ft.TextField(
            label="Materia",
            width=400
        )

        self.txt_nombre = ft.TextField(
            label="Nombre del alumno",
            width=400
        )

        self.chk_presente = ft.Checkbox(
            label="Presente"
        )

        self.btn_registrar = ft.ElevatedButton(
            "Registrar asistencia",
            width=250
        )

        self.btn_limpiar = ft.ElevatedButton(
            "Nueva clase-Limpiar registro",
            width=250
        )

        self.lbl_mensaje = ft.Text(
            value="",
            size=10
        )

        self.lista_registros = ft.Column()

    def construirinterfaz(self):

        return ft.Column([

            ft.Text(
                "Registro de asistencia",
                size=30,
                weight=ft.FontWeight.BOLD,
            ),

            ft.Divider(),

            self.txt_grupo,
            self.txt_materia,
            self.txt_nombre,
            self.chk_presente,

            self.btn_registrar,
            self.btn_limpiar,

            self.lbl_mensaje,

            ft.Text(
                "Lista de registros",
                size=20,
                weight=ft.FontWeight.BOLD,
            ),

            self.lista_registros
        ])

    def agregar_Texto(self, texto):
        return ft.Text(value=texto, size=16)