from gui.dialogs import mostrar_excepcion
import core.reconocimiento as reconocimiento

def on_nuevo_usuario():
    try:
        reconocimiento.empezar_reconocimiento_facial()
    except Exception as e:
        mostrar_excepcion(e)