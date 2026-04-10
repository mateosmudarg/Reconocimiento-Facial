from gui.dialogs import mostrar_excepcion
import gui.camara as camara

def on_nuevo_usuario():
    try:
        camara.iniciar_reconocimiento()
    except Exception as e:
        mostrar_excepcion(e)