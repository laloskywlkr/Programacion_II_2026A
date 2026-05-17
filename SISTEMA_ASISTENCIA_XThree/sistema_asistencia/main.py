import flet as ft
from vista.asistenciaView import AsistenciaView
from controller.asistenciaController import AsistenciaController

def main(page: ft.Page):

    vista = AsistenciaView(page)

    controller = AsistenciaController(vista)

    vista.btn_registrar.on_click = controller.registrarAsistencia
    vista.btn_limpiar.on_click = controller.limpiarCampos

    page.add(
        vista.construirinterfaz()
    )

ft.app(target=main)